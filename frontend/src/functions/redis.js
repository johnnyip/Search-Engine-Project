const axios = require('axios');

export const saveRedis = async (id, value) => {
    let status = false
    let url = (process.env.REACT_APP_BACKEND1_URL !== undefined) ? process.env.REACT_APP_BACKEND1_URL : 'http://localhost:8080'
    url += '/redis/save?id=' + id

    await axios.post(url, value)
        .then((response) => {
            if (response.status === 200) {
                status = true
            }
            // console.log(response)
        })
        .catch((err) => {
            console.error(err)
        })

    return status
}

export const getRedis = async (id) => {
    let result = []
    let url = (process.env.REACT_APP_BACKEND1_URL !== undefined) ? process.env.REACT_APP_BACKEND1_URL : 'http://localhost:8080'
    url += '/redis/get?id=' + id

    await axios.get(url)
        .then((response) => {
            if (response.status === 200) {
                result = response.data
            }
            // console.log(response)
        })
        .catch((err) => {
            console.error(err)
        })

    return result
}

