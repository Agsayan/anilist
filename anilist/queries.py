READING_STATUS = """
    query ($page: Int, $perPage: Int, $id: Int) {
        Page(page: $page, perPage: $perPage) {
          pageInfo {
            total
            perPage
          }
          media(id: $id) {
            episodes
            chapters
            status
          }
        }
      }
"""


SEARCH_IMAGES = """
    query ($page: Int, $perPage: Int, $id: Int, $type: MediaType) {
    Page(page: $page, perPage: $perPage) {
      pageInfo {
        total
        perPage
      }
      media(id: $id, type: $type, sort: FAVOURITES_DESC) {
        id
        coverImage {
            large
            medium
        }
        bannerImage
      }
    }
  }
"""


SEARCH_QUERY_ID = """
    query ($page: Int, $perPage: Int, $id: Int, $type: MediaType) {
    Page(page: $page, perPage: $perPage) {
      pageInfo {
        total
        perPage
      }
      media(id: $id, type: $type, sort: FAVOURITES_DESC) {
        id
        synonyms
        type
        title {
            romaji
            english
        }
        startDate {
            year
            month
            day
        }
        endDate {
            year
            month
            day
        }
        coverImage {
            large
        }
        tags {
            name
        }
        bannerImage
        format
        chapters
        volumes
        status
        description
        averageScore
        meanScore
        genres
        synonyms
      }
    }
  }
    """

SEARCH_QUERY = """
    query ($page: Int, $perPage: Int, $search: String, $type: MediaType) {
    Page(page: $page, perPage: $perPage) {
      pageInfo {
        total
        perPage
      }
      media(search: $search, type: $type, sort: FAVOURITES_DESC) {
        id
        synonyms
        type
        title {
            romaji
            english
        }
        startDate {
            year
            month
            day
        }
        endDate {
            year
            month
            day
        }
        coverImage {
            large
        }
        tags {
            name
        }
        bannerImage
        format
        chapters
        volumes
        status
        description
        averageScore
        meanScore
        genres
        synonyms
      }
    }
  }
    """


UPDATE_QUERY = """
    mutation ($mediaId: Int, $status: MediaListStatus, $progress: Int) {
        SaveMediaListEntry (mediaId: $mediaId, status: $status, progress: $progress ) {
            id
            status
            progress
        }
    }
"""

MANGA_LIST_COLLECTION = """
query MangaListCollectionQuery(
    $userId: Int
) {
    MediaListCollection(
        userId: $userId,
        type: MANGA
    ) {
        lists {
            entries {
                id
                status
                score
                progress
                progressVolumes
                repeat
                priority
                private
                notes
                hiddenFromStatusLists
                customLists
                advancedScores
                startedAt {
                    year
                    month
                    day
                }
                completedAt {
                    year
                    month
                    day
                }
                updatedAt
                createdAt
                media {
                    id
                    title {
                        romaji
                        english
                        native
                        userPreferred
                    }
                    type
                    format
                    status(version: 2)
                    startDate {
                        year
                        month
                        day
                    }
                    chapters
                    volumes
                    countryOfOrigin
                    source
                    isFavourite
                    coverImage {
                        large
                    }
                    genres
                    synonyms
                    averageScore
                    popularity
                    tags {
                        name
                    }
                    isAdult
                    externalLinks {
                        site
                    }
                }
            }
            name
            isCustomList
            isSplitCompletedList
            status
        }
    }
}
"""

SEARCH_USER = """
query SearchUsersQuery(
    $page: Int,
    $search: String,
    $sort: [UserSort]
) {
    Page(page: $page) {
        pageInfo {
            total
            perPage
            currentPage
            lastPage
            hasNextPage
        }
        users(search: $search, sort: $sort) {
            id
            name
            avatar {
                large
            }
        }
    }
}
"""
