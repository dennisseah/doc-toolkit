from unittest.mock import MagicMock

import azure.ai.formrecognizer as fr
import pytest
from pytest_mock import MockerFixture

import extractors.azure_form_recognizer as extractor

TBL_BOUNDING_REGIONS = [
    fr.BoundingRegion(page_number=1, polygon=[fr.Point(x=1, y=1)]),
    fr.BoundingRegion(page_number=1, polygon=[fr.Point(x=1, y=2)]),
    fr.BoundingRegion(page_number=1, polygon=[fr.Point(x=2, y=1)]),
    fr.BoundingRegion(page_number=1, polygon=[fr.Point(x=2, y=2)]),
]


@pytest.mark.unit
@pytest.mark.asyncio
async def test_extractor(mocker: MockerFixture):
    # arrange
    fr_result = MagicMock()
    fr_result.tables = [
        fr.DocumentTable(
            row_count=2,
            column_count=2,
            cells=[
                fr.DocumentTableCell(
                    row_index=0,
                    column_index=0,
                    content="cell0_0",
                    bounding_regions=[TBL_BOUNDING_REGIONS[0]],
                ),
                fr.DocumentTableCell(
                    row_index=0,
                    column_index=1,
                    content="cell0_1",
                    bounding_regions=[TBL_BOUNDING_REGIONS[1]],
                ),
                fr.DocumentTableCell(
                    row_index=1,
                    column_index=0,
                    content="cell1_0",
                    bounding_regions=[TBL_BOUNDING_REGIONS[2]],
                ),
                fr.DocumentTableCell(
                    row_index=1,
                    column_index=1,
                    content="cell1_1",
                    bounding_regions=[TBL_BOUNDING_REGIONS[3]],
                ),
            ],
        )
    ]
    fr_result.paragraphs = [
        fr.DocumentParagraph(
            role="pageHeader",
            content="header",
            bounding_regions=[
                fr.BoundingRegion(page_number=1, polygon=[fr.Point(x=0.5, y=0.5)])
            ],
        ),
        fr.DocumentParagraph(
            content="paragraph0",
            bounding_regions=[
                fr.BoundingRegion(page_number=1, polygon=[fr.Point(x=0, y=0)])
            ],
        ),
        fr.DocumentParagraph(
            content="cell0_0",
            bounding_regions=[TBL_BOUNDING_REGIONS[0]],
        ),
        fr.DocumentParagraph(
            content="cell0_1",
            bounding_regions=[TBL_BOUNDING_REGIONS[1]],
        ),
        fr.DocumentParagraph(
            content="cell1_0",
            bounding_regions=[TBL_BOUNDING_REGIONS[2]],
        ),
        fr.DocumentParagraph(
            content="cell1_1",
            bounding_regions=[TBL_BOUNDING_REGIONS[3]],
        ),
        fr.DocumentParagraph(
            content="second page",
            bounding_regions=[
                fr.BoundingRegion(page_number=2, polygon=[fr.Point(x=0.5, y=0.5)])
            ],
        ),
        fr.DocumentParagraph(
            content="no bounding regions",
            bounding_regions=[],
        ),
    ]
    mocker.patch("extractors.azure_form_recognizer.analyze", return_value=fr_result)

    # act
    result = await extractor.extract(
        settings=MagicMock(),
        sas_url="sas_url",
        discard_roles=[extractor.ParagraphRole(role="pageHeader")],
    )

    # assert
    assert """paragraph0

| cell0_0   | cell0_1   |
|-----------|-----------|
| cell1_0   | cell1_1   |

second page

no bounding regions""" == result
