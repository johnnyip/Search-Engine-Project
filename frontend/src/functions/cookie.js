export const saveHistory = (token) => {
    document.cookie = `history=${token}`;

    if (getCookie("history") === "") {
        alert("Cannot save cookie. Please allow it in browser setting.")
    }
}

export const removeHistory = () => {
    document.cookie = `history=`;
}

export const getHistory = () => {
    return getCookie("history")
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
            return result.length !== 0 ? JSON.parse(result) : [];
        }
    }
    return [];
}  
