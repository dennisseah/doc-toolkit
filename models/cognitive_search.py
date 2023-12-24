from pydantic import BaseModel


class CognitiveSearchResponseQueryContext(BaseModel):
    original_query: str
    ask_user_for_location: bool | None = None


class CognitiveSearchWebImageObject(BaseModel):
    thumbnail_url: str
    width: int
    height: int


class CognitiveSearchWebPage(BaseModel):
    name: str
    url: str
    id: str | None = None
    thumbnail_url: str | None = None
    display_url: str | None = None
    snippet: str | None = None
    date_last_crawled: str | None = None
    deep_links: list["CognitiveSearchWebPage"] = []
    primary_image_of_page: CognitiveSearchWebImageObject | None = None


class CognitiveSearchImageThumbnail(BaseModel):
    width: int
    height: int


class CognitiveSearchImageObject(BaseModel):
    web_search_url: str
    name: str
    thumbnail_url: str
    content_url: str
    host_page_url: str
    width: int
    height: int
    thumbnail: CognitiveSearchImageThumbnail


class CognitiveSearchImages(BaseModel):
    id: str
    web_search_url: str
    is_family_friendly: bool
    value: list[CognitiveSearchImageObject]


class CognitiveSearchWebAnswer(BaseModel):
    web_search_url: str
    total_estimated_matches: int
    value: list[CognitiveSearchWebPage]


class CognitiveSearchRelatedSearchAnswer(BaseModel):
    text: str
    display_text: str
    web_search_url: str


class CognitiveSearchRelatedSearchAnswers(BaseModel):
    id: str
    value: list[CognitiveSearchRelatedSearchAnswer]


class CognitiveSearchVideo(BaseModel):
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
    thumbnail: CognitiveSearchImageThumbnail
    allow_mobile_embed: bool
    is_superfresh: bool


class CognitiveSearchVideos(BaseModel):
    id: str
    web_search_url: str
    is_family_friendly: bool
    value: list[CognitiveSearchVideo]


class CognitiveSearchRankingResponseMainLineItemValue(BaseModel):
    id: str


class CognitiveSearchRankingResponseMainLineItem(BaseModel):
    answer_type: str
    result_index: int | None = None
    value: CognitiveSearchRankingResponseMainLineItemValue


class CognitiveSearchRankingResponseMainLine(BaseModel):
    items: list[CognitiveSearchRankingResponseMainLineItem]


class CognitiveSearchRankingResponseSidebarItemValue(BaseModel):
    id: str


class CognitiveSearchRankingResponseSidebarItem(BaseModel):
    answer_type: str
    result_index: int | None = None
    value: CognitiveSearchRankingResponseSidebarItemValue | None = None


class CognitiveSearchRankingResponseSidebar(BaseModel):
    items: list[CognitiveSearchRankingResponseSidebarItem]


class CognitiveSearchRankingResponse(BaseModel):
    mainline: CognitiveSearchRankingResponseMainLine
    sidebar: CognitiveSearchRankingResponseSidebar


class CognitiveSearchResponse(BaseModel):
    query_context: CognitiveSearchResponseQueryContext
    web_pages: CognitiveSearchWebAnswer
    related_searches: CognitiveSearchRelatedSearchAnswers
    images: CognitiveSearchImages | None = None
    videos: CognitiveSearchVideos | None = None
    ranking_response: CognitiveSearchRankingResponse
