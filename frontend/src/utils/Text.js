function formatName(str) {
    str = str.toLowerCase()
    return str.replace(/\b\w/g, match => match.toUpperCase());
}

export default formatName