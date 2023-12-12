from typing import Literal

import azure.ai.formrecognizer as fr
from pydantic import BaseModel
from tabulate import tabulate

from common.settings import Settings
from services.azure_form_recognizer import analyze

# Extract textual content from a document
# Tables will be added in place in the page and formatted in markdown format
# for example
# | Header 1 | Header 2 |
# | -------- | -------- |
# | Cell 1   | Cell 2   |
# | Cell 3   | Cell 4   |


class ParagraphRole(BaseModel):
    role: Literal["pageHeader", "pageFooter", "pageNumber"]


class DocTableCell(BaseModel):
    page_number: int
    row_index: int
    column_index: int
    text: str
    x: float
    y: float


class DocTable(BaseModel):
    cells: list[DocTableCell]
    displayed: bool = False

    def in_range(self, input: list[fr.BoundingRegion] | None) -> bool:
        if not input or self.cells[0].page_number != input[0].page_number:
            return False

        def cmp(cell: DocTableCell, r2: list[fr.BoundingRegion] | None) -> bool:
            _r2 = r2[0]  # type: ignore
            return cell.x == _r2.polygon[0].x and cell.y == _r2.polygon[0].y

        for cell in self.cells:
            if cmp(cell, input):
                return True

        return False

    def format(self) -> str:
        self.cells.sort(key=lambda x: x.row_index)
        cur_row = 0
        buckets = [[]]

        for cell in self.cells:
            if cell.row_index != cur_row:
                buckets.append([])
                cur_row += 1
            buckets[cur_row].append(cell.text)

        header = buckets.pop(0)
        return tabulate(buckets, headers=header, tablefmt="github")


def get_tables(fr_result: fr.AnalyzeResult) -> list[DocTable]:
    tables = []

    if fr_result.tables:
        for tbl in fr_result.tables:
            cells = []
            for cell in tbl.cells:
                bounding_regions = cell.bounding_regions[0]  # type: ignore

                cells.append(
                    DocTableCell(
                        text=cell.content,
                        row_index=cell.row_index,
                        column_index=cell.column_index,
                        page_number=bounding_regions.page_number,
                        x=bounding_regions.polygon[0].x,
                        y=bounding_regions.polygon[0].y,
                    )
                )
            tables.append(DocTable(cells=cells))

    return tables


def format_result(
    fr_result: fr.AnalyzeResult, discard_roles: list[ParagraphRole]
) -> str:
    content = []
    tables = get_tables(fr_result)

    def in_table(paragraph: fr.DocumentParagraph) -> DocTable | None:
        return next(
            (tbl for tbl in tables if tbl.in_range(paragraph.bounding_regions)), None
        )

    drop_roles = [role.role for role in discard_roles]

    if fr_result.paragraphs:
        for paragraph in filter(
            lambda x: x.role not in drop_roles, fr_result.paragraphs
        ):
            tbl = in_table(paragraph)
            if tbl:
                if not tbl.displayed:
                    content.append(tbl.format())
                    tbl.displayed = True
            else:
                content.append(paragraph.content)

    return "\n\n".join(content)


async def extract(
    settings: Settings, sas_url: str, discard_roles: list[ParagraphRole] = []
) -> str:
    """Extract textual content from a document.

    :param settings: Settings object
    :param sas_url: SAS URL of the document
    :param discard_roles: List of roles to discard
    """
    fr_result = await analyze(settings, sas_url)
    return format_result(fr_result, discard_roles)
