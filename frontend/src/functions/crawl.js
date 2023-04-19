const axios = require('axios');

export const javaStatus = async () => {
    let status = false
    let url = (process.env.REACT_APP_BACKEND1_URL !== undefined) ? process.env.REACT_APP_BACKEND1_URL : 'http://localhost:8080'

    await axios.get(url)
        .then((response) => {
            if (response.status === 200) {
                status = true
            }
        })
        .catch((err) => {
            console.error(err)
        })

    return status
}

export const checkIndexStat = async () => {
    let result = 0
    let url = (process.env.REACT_APP_BACKEND1_URL !== undefined) ? process.env.REACT_APP_BACKEND1_URL : 'http://localhost:8080'
    // let url = (process.env.REACT_APP_SERVER_URL !== undefined) ? process.env.REACT_APP_SERVER_URL : 'https://search-back1.johnnyip.com'
    url += '/crawl/stat'

    await axios.get(url)
        .then((response) => {
            if (response.status === 200) {
                result = response.data
                console.log(result)
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
    let url = (process.env.REACT_APP_BACKEND1_URL !== undefined) ? process.env.REACT_APP_BACKEND1_URL : 'http://localhost:8080'
    url += '/crawl/start?url=' + crawl_url

    await axios.get(url, { timeout: 2000 * 60 * 60 })
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
    let url = (process.env.REACT_APP_BACKEND1_URL !== undefined) ? process.env.REACT_APP_BACKEND1_URL : 'http://localhost:8080'
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
