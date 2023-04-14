const axios = require('axios');

export const pythonStatus = async () => {
    let status = false
    let url = (process.env.REACT_APP_BACKEND2_URL !== undefined) ? process.env.REACT_APP_BACKEND2_URL : 'http://localhost:5000'
    // let url = 'http://localhost:5000'

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

export const queryVector = async (keyword) => {
    let result = 0
    console.log("vector")
    let url = (process.env.REACT_APP_BACKEND2_URL !== undefined) ? process.env.REACT_APP_BACKEND2_URL : 'http://localhost:5000'
    // let url = (process.env.REACT_APP_SERVER_URL !== undefined) ? process.env.REACT_APP_SERVER_URL : 'http://127.0.0.1:5000'
    url += '/query_vector?keyword=' + encodeURIComponent(keyword)

    await axios.get(url)
        .then((response) => {
            if (response.status === 200) {
                result = response.data

                const resultArray = Object.keys(result.data.result).map(item => ({
                    url: item,
                    score: result.data.result[item]
                }));
                resultArray.sort((a, b) => b.score - a.score);

                result.data.result = resultArray;

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

export const queryPageRank = async (keyword) => {
    let result = 0
    console.log("pagerank")
    let url = (process.env.REACT_APP_BACKEND2_URL !== undefined) ? process.env.REACT_APP_BACKEND2_URL : 'http://localhost:5000'
    // let url = (process.env.REACT_APP_SERVER_URL !== undefined) ? process.env.REACT_APP_SERVER_URL : 'http://127.0.0.1:5000'
    url += '/query_pagerank?keyword=' + encodeURIComponent(keyword)

    await axios.get(url)
        .then((response) => {
            if (response.status === 200) {
                result = response.data

                const resultArray = Object.keys(result.data.result).map(item => ({
                    url: item,
                    score: result.data.result[item]
                }));
                resultArray.sort((a, b) => b.score - a.score);

                result.data.result = resultArray;
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

export const querySemantics = async (keyword) => {
    let result = 0
    console.log("semantics")
    let url = (process.env.REACT_APP_BACKEND2_URL !== undefined) ? process.env.REACT_APP_BACKEND2_URL : 'http://localhost:5000'
    // let url = (process.env.REACT_APP_SERVER_URL !== undefined) ? process.env.REACT_APP_SERVER_URL : 'http://127.0.0.1:5000'
    url += '/query_semantics?keyword=' + encodeURIComponent(keyword)

    await axios.get(url)
        .then((response) => {
            if (response.status === 200) {
                result = response.data

                const newArray = result.data.result.map(([url, score]) => ({ url, score }));
                newArray.sort((a, b) => b.score - a.score);

                result.data.result = newArray;

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

