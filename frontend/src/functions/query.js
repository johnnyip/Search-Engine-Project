const axios = require('axios');

export const queryVector = async (keyword) => {
    let result = 0
    // let url = (process.env.REACT_APP_SERVER_URL !== undefined) ? process.env.REACT_APP_SERVER_URL : 'https://search-back2.johnnyip.com'
    let url = (process.env.REACT_APP_SERVER_URL !== undefined) ? process.env.REACT_APP_SERVER_URL : 'http://127.0.0.1:5000'
    url += '/query_vector?keyword=' + encodeURIComponent(keyword)

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

