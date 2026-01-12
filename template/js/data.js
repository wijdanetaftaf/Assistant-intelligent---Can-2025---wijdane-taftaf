async function loadCSV(path) {
    const res = await fetch(path);
    const text = await res.text();

    const [header, ...rows] = text.split("\n").filter(Boolean);
    const keys = header.split(",");

    return rows.map(row => {
        const values = row.split(/,(?=(?:(?:[^"]*"){2})*[^"]*$)/);
        const obj = {};
        keys.forEach((k, i) => {
            obj[k.trim()] = values[i]?.replace(/"/g, "").trim();
        });
        return obj;
    });
}

function cleanNumber(value) {
    if (!value) return 0;
    return parseInt(
        value
            .toString()
            .replace(/\s/g, "")
            .replace(",", "")
    ) || 0;
}
