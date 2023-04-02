const axios = require('axios');

export const checkCrawlPageCount = async () => {
    let result = 0
    let url = (process.env.REACT_APP_SERVER_URL !== undefined) ? process.env.REACT_APP_SERVER_URL : 'https://search-back1.johnnyip.com'
    url += '/crawl/count'

    await axios.get(url)
        .then((response) => {
            if (response.status === 200) {
                result = response.data
            } else {
                result = 0
            }
        })
        .catch((err) => {
            console.error(err)
            result = false
        })

    return result
}

export const startCrawl = async (crawl_url) => {
    let result = 0
    let url = (process.env.REACT_APP_SERVER_URL !== undefined) ? process.env.REACT_APP_SERVER_URL : 'https://search-back1.johnnyip.com'
    url += '/crawl/start?url=' + crawl_url

    await axios.get(url)
        .then((response) => {
            if (response.status === 200) {
                result = response.data
            } else {
                result = 0
            }
        })
        .catch((err) => {
            console.error(err)
            result = false
        })

    return result
}


export const removeCrawlContent = async (crawl_url) => {
    let result = 0
    let url = (process.env.REACT_APP_SERVER_URL !== undefined) ? process.env.REACT_APP_SERVER_URL : 'https://search-back1.johnnyip.com'
    url += '/crawl/remove'

    await axios.get(url)
        .then((response) => {
            if (response.status === 200) {
                result = response.data
            } else {
                result = 0
            }
        })
        .catch((err) => {
            console.error(err)
            result = false
        })

    return result
}
