from pydantic import BaseModel


class BingSearchResponseQueryContext(BaseModel):
    original_query: str
    ask_user_for_location: bool | None = None


class BingSearchWebImageObject(BaseModel):
    thumbnail_url: str
    width: int
    height: int


class BingSearchWebPage(BaseModel):
    name: str
    url: str
    id: str | None = None
    thumbnail_url: str | None = None
    display_url: str | None = None
    snippet: str | None = None
    date_last_crawled: str | None = None
    deep_links: list["BingSearchWebPage"] = []
    primary_image_of_page: BingSearchWebImageObject | None = None


class BingSearchImageThumbnail(BaseModel):
    width: int
    height: int


class BingSearchImageObject(BaseModel):
    web_search_url: str
    name: str
    thumbnail_url: str
    content_url: str
    host_page_url: str
    width: int
    height: int
    thumbnail: BingSearchImageThumbnail


class BingSearchImages(BaseModel):
    id: str
    web_search_url: str
    is_family_friendly: bool
    value: list[BingSearchImageObject]


class BingSearchWebAnswer(BaseModel):
    web_search_url: str
    total_estimated_matches: int
    value: list[BingSearchWebPage]


class BingSearchRelatedSearchAnswer(BaseModel):
    text: str
    display_text: str
    web_search_url: str


class BingSearchRelatedSearchAnswers(BaseModel):
    id: str
    value: list[BingSearchRelatedSearchAnswer]


class BingSearchVideo(BaseModel):
    web_search_url: str
    name: str
    description: str
    thumbnail_url: str
    content_url: str
    host_page_url: str
    width: int
    height: int
    motion_thumbnail_url: str
    embed_html: str
    allow_https_embed: bool
    view_count: int
    thumbnail: BingSearchImageThumbnail
    allow_mobile_embed: bool
    is_superfresh: bool


class BingSearchVideos(BaseModel):
    id: str
    web_search_url: str
    is_family_friendly: bool
    value: list[BingSearchVideo]


class BingSearchRankingResponseMainLineItemValue(BaseModel):
    id: str


class BingSearchRankingResponseMainLineItem(BaseModel):
    answer_type: str
    result_index: int | None = None
    value: BingSearchRankingResponseMainLineItemValue


class BingSearchRankingResponseMainLine(BaseModel):
    items: list[BingSearchRankingResponseMainLineItem]


class BingSearchRankingResponseSidebarItemValue(BaseModel):
    id: str


class BingSearchRankingResponseSidebarItem(BaseModel):
    answer_type: str
    result_index: int | None = None
    value: BingSearchRankingResponseSidebarItemValue | None = None


class BingSearchRankingResponseSidebar(BaseModel):
    items: list[BingSearchRankingResponseSidebarItem]


class BingSearchRankingResponse(BaseModel):
    mainline: BingSearchRankingResponseMainLine
    sidebar: BingSearchRankingResponseSidebar


class BingSearchResponse(BaseModel):
    query_context: BingSearchResponseQueryContext
    web_pages: BingSearchWebAnswer
    related_searches: BingSearchRelatedSearchAnswers
    images: BingSearchImages | None = None
    videos: BingSearchVideos | None = None
    ranking_response: BingSearchRankingResponse
