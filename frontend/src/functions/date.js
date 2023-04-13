export function formatDate(date) {
    const addLeadingZero = (num) => (num < 10 ? '0' : '') + num;

    const day = addLeadingZero(date.getDate());
    const month = addLeadingZero(date.getMonth() + 1); // Months are 0-based
    const year = date.getFullYear().toString().slice(-2);
    const hours = addLeadingZero(date.getHours());
    const minutes = addLeadingZero(date.getMinutes());
    const seconds = addLeadingZero(date.getSeconds());

    return `${day}/${month}/${year} ${hours}:${minutes}:${seconds}`;
}