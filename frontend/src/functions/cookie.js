export const saveHistoryToken = (token) => {
    document.cookie = `historyToken=${token}`;

    if (getCookie("historyToken") === "") {
        alert("Cannot save cookie. Please allow it in browser setting.")
    }
}

export const getHistoryToken = () => {
    let token = getCookie("historyToken")
    if (token === "") {
        token = makeid(10)
        saveHistoryToken(token)
    }
    return token
}

function getCookie(cname) {
    let name = cname + "=";
    let ca = document.cookie.split(';');
    for (let i = 0; i < ca.length; i++) {
        let c = ca[i];
        while (c.charAt(0) === ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) === 0) {
            let result = c.substring(name.length, c.length)
            return result.length !== 0 ? result : "";
        }
    }
    return "";
}

function makeid(length) {
    let result = '';
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const charactersLength = characters.length;
    let counter = 0;
    while (counter < length) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
        counter += 1;
    }
    return result;
}
