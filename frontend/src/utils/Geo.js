function calculateDistance(lat1, lon1, lat2, lon2) {
    const earthRadiusKm = 6371;
    const dLat = toRadians(lat2 - lat1);
    const dLon = toRadians(lon2 - lon1);

    const a =
        Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(toRadians(lat1)) * Math.cos(toRadians(lat2)) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2);

    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

    return earthRadiusKm * c;
}

function calculateCenter(lat1, lon1, lat2, lon2) {
    const centerLat = (lat1 + lat2) / 2;
    const centerLon = (lon1 + lon2) / 2;
    return [centerLat, centerLon];
}

function toRadians(degrees) {
    return degrees * (Math.PI / 180);
}

export {calculateDistance, calculateCenter}