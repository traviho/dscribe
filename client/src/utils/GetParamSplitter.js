export function getParamSplitter(paramArr) {
    if (paramArr.length === 0) {
        return ""
    } else if (paramArr.length === 1) {
        return `${paramArr[0].value}`
    }
    let res = paramArr[0].value;
    for (let i = 1; i < paramArr.length; i++) {
        res += `,${paramArr[i].value}`;
    }
    return res;
}

export function nullOrEmpty(obj) {
    return obj == null || obj.length === 0;
}