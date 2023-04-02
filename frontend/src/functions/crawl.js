const axios = require('axios');

export const checkCrawlPageCount = async () => {
    let result = 0
    let url = (process.env.REACT_APP_SERVER_URL !== undefined) ? process.env.REACT_APP_SERVER_URL : 'https://search-back1.johnnyip.com'
    url += '/crawl/count'

    await axios.get(url)
        .then((response) => {
            console.log(response)
            if (response.status === 200 && response.data === "Hello world") {
                result = 1
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
