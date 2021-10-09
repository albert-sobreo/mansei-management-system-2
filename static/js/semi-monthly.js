function semi_months(year){
    start1 = '26'
    end1 = '10'
    start2 = '11'
    end2 = '25'

    dates = [
        [`${year-1}-12-${start1}`, `${year}-1-${end1}`, `Dec. ${start1}, ${year-1}`, `Jan. ${end1}, ${year}`],
        [`${year}-1-${start2}`, `${year}-1-${end2}`, `Jan. ${start2}, ${year}`, `Jan. ${end2}, ${year}`],
        [`${year}-1-${start1}`, `${year}-2-${end1}`, `Jan. ${start1}, ${year}`, `Feb. ${end1}, ${year}`],
        [`${year}-2-${start2}`, `${year}-2-${end2}`, `Feb. ${start2}, ${year}`, `Feb. ${end2}, ${year}`],
        [`${year}-2-${start1}`, `${year}-3-${end1}`, `Feb. ${start1}, ${year}`, `Mar. ${end1}, ${year}`],
        [`${year}-3-${start2}`, `${year}-3-${end2}`, `Mar. ${start2}, ${year}`, `Mar. ${end2}, ${year}`],
        [`${year}-3-${start1}`, `${year}-4-${end1}`, `Mar. ${start1}, ${year}`, `Apr. ${end1}, ${year}`],
        [`${year}-4-${start2}`, `${year}-4-${end2}`, `Apr. ${start2}, ${year}`, `Apr. ${end2}, ${year}`],
        [`${year}-4-${start1}`, `${year}-5-${end1}`, `Apr. ${start1}, ${year}`, `May ${end1}, ${year}`],
        [`${year}-5-${start2}`, `${year}-5-${end2}`, `May ${start2}, ${year}`, `May ${end2}, ${year}`],
        [`${year}-5-${start1}`, `${year}-6-${end1}`, `May ${start1}, ${year}`, `Jun. ${end1}, ${year}`],
        [`${year}-6-${start2}`, `${year}-6-${end2}`, `Jun. ${start2}, ${year}`, `Jun. ${end2}, ${year}`],
        [`${year}-6-${start1}`, `${year}-7-${end1}`, `Jun. ${start1}, ${year}`, `Jul. ${end1}, ${year}`],
        [`${year}-7-${start2}`, `${year}-7-${end2}`, `Jul. ${start2}, ${year}`, `Jul. ${end2}, ${year}`],
        [`${year}-7-${start1}`, `${year}-8-${end1}`, `Jul. ${start1}, ${year}`, `Aug. ${end1}, ${year}`],
        [`${year}-8-${start2}`, `${year}-8-${end2}`, `Aug. ${start2}, ${year}`, `Aug. ${end2}, ${year}`],
        [`${year}-8-${start1}`, `${year}-9-${end1}`, `Aug. ${start1}, ${year}`, `Sep. ${end1}, ${year}`],
        [`${year}-9-${start2}`, `${year}-9-${end2}`, `Sep. ${start2}, ${year}`, `Sep. ${end2}, ${year}`],
        [`${year}-9-${start1}`, `${year}-10-${end1}`, `Sep. ${start1}, ${year}`, `Oct. ${end1}, ${year}`],
        [`${year}-10-${start2}`, `${year}-10-${end2}`, `Oct. ${start2}, ${year}`, `Oct. ${end2}, ${year}`],
        [`${year}-10-${start1}`, `${year}-11-${end1}`, `Oct. ${start1}, ${year}`, `Nov. ${end1}, ${year}`],
        [`${year}-11-${start2}`, `${year}-11-${end2}`, `Nov. ${start2}, ${year}`, `Nov. ${end2}, ${year}`],
        [`${year}-11-${start1}`, `${year}-12-${end1}`, `Nov. ${start1}, ${year}`, `Dec. ${end1}, ${year}`],
        [`${year}-12-${start2}`, `${year}-12-${end2}`, `Dec. ${start2}, ${year}`, `Dec. ${end2}, ${year}`],
    ]

    return dates

}