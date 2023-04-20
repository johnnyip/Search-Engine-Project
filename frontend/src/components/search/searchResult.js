import { useState, useEffect } from 'react'
import { Pagination, Select, Group, Button } from '@mantine/core';
import { IconFilter, IconArrowUp, IconArrowDown } from '@tabler/icons-react';

import ResultItem from './resultItem'

const SearchResult = (props) => {
    let result = props.result
    const itemPerPage = 5;
    const sortOptions_term = [
        { label: "Default (Score)", value: "" },
        { label: "Page Size", value: "size" },
        { label: "Filtered Term Frequency", value: "term" },
        { label: "Rank of Filtered Term Frequency In Document", value: "termRank" },
        { label: "Last Modified Date", value: "date" },
        { label: "Number of Parents", value: "parent" },
        { label: "Number of Children", value: "child" },

    ]
    const sortOptions_noTerm = [
        { label: "Default (Score)", value: "" },
        { label: "Page Size", value: "size" },
        { label: "Last Modified Date", value: "date" },
        { label: "Number of Parents", value: "parent" },
        { label: "Number of Children", value: "child" },
    ]

    const [activePage, setPage] = useState(1);
    const [resultInPage, setResultInPage] = useState([])
    const [completeFilteredResult, setCompleteFilteredResult] = useState([])
    const [ascending, setAscending] = useState(false)

    const [showFilter, setShowFilter] = useState(false)
    const [filterTerm, setFilterTerm] = useState("")
    const [sortOption, setSortOption] = useState("")
    const [termsArray, setTermsArray] = useState([])

    const extractDocumentTerms = () => {
        //Extract all terms in the document
        let uniqueTerms = new Map()
        let uniqueTermsArray = [{
            "label": "None",
            "value": ""
        }]
        if (Object.keys(result).length !== 0) {
            for (let result_ of result.data.result) {
                result_ = result_["Most Frequent Items"]
                for (let term of result_) {
                    //Check if the object is existed in the array
                    if (!uniqueTerms.has(term.Item)) {
                        uniqueTerms.set(term.Item, 1)
                    } else {
                        uniqueTerms.set(term.Item, uniqueTerms.get(term.Item) + 1)
                    }
                }
            }

            //Sort the uniqueTerms by the value
            uniqueTerms = new Map([...uniqueTerms.entries()].sort((a, b) => b[1] - a[1]))
            uniqueTerms.forEach((item, key) => {
                uniqueTermsArray.push({
                    "label": `${key} (${item} Documents)`,
                    "value": key
                })
            })
            // console.log(uniqueTerms)
            // console.log(uniqueTermsArray)
            setTermsArray(uniqueTermsArray)
        }
    }

    const extractResultInPage = async () => {
        let result_ = []

        //Filter out the result by terms
        if (filterTerm === "") {
            result_ = result.data.result
        } else {
            for (let item of result.data.result) {
                if (item["Most Frequent Items"].map((item) => item.Item).indexOf(filterTerm) !== -1) {
                    result_.push(item)
                }
            }
        }


        // console.log(sortOption)
        // console.log(result_)
        //Sort the result by the sortOption
        if (sortOption === "") {
            //Sort by Score
            result_ = result_.sort((a, b) => b.Score - a.Score)
        } else if (sortOption === "size") {
            result_ = result_.sort((a, b) => b["Size of the Page"] - a["Size of the Page"])
        } else if (sortOption === "term" && filterTerm !== "") {
            result_ = result_.sort((a, b) => {
                let aTerm = a["Most Frequent Items"].filter((item) => item.Item === filterTerm)[0]
                let bTerm = b["Most Frequent Items"].filter((item) => item.Item === filterTerm)[0]
                return bTerm.Frequency - aTerm.Frequency
            })
        } else if (sortOption === "termRank" && filterTerm !== "") {
            //Sort the result by the position in the array of "Most Frequent Items"
            result_ = result_.sort((a, b) => {
                let aTerm = a["Most Frequent Items"].map((item) => item.Item).indexOf(filterTerm)
                let bTerm = b["Most Frequent Items"].map((item) => item.Item).indexOf(filterTerm)
                return aTerm - bTerm
            })
        } else if (sortOption === "date") {
            result_ = result_.sort((a, b) => {
                let aDate = new Date(a["Last Modified Date"])
                let bDate = new Date(b["Last Modified Date"])
                return bDate - aDate
            })
        } else if (sortOption === "parent") {
            result_ = result_.sort((a, b) => b["Parent Link"].length - a["Parent Link"].length)
        } else if (sortOption === "child") {
            result_ = result_.sort((a, b) => b["Child Link"].length - a["Child Link"].length)
        }

        //Sort the result by the ascending order
        if (ascending) {
            result_ = result_.reverse()
        }
        // console.log(result_)
        setCompleteFilteredResult(result_)
    }

    const pagination = (result_) => {
        let start = (activePage - 1) * itemPerPage;
        let end = start + itemPerPage;
        let dataInPage
        if (result_ === undefined) {
            dataInPage = completeFilteredResult.slice(start, end)
        } else {
            dataInPage = result_.slice(start, end)
        }
        setResultInPage(dataInPage)
    }

    useEffect(() => {
        if (Object.keys(result).length !== 0) {
            extractDocumentTerms();
            extractResultInPage();
            setPage(1);
            setFilterTerm("");
        }
    }, [result]);

    useEffect(() => {
        if (Object.keys(result).length !== 0) {
            extractResultInPage()
            pagination()
        }
    }, [filterTerm, sortOption, ascending])

    useEffect(() => {
        pagination()
    }, [activePage, completeFilteredResult]);


    if (Object.keys(result).length !== 0) {
        return (
            <>
                <Group position='center'>
                    <b>{result.data.result.length} results ({result.data.time})</b>
                    <Button
                        leftIcon={<IconFilter height={20} width={20} />}
                        onClick={() => setShowFilter(!showFilter)}>
                        {showFilter ? "Hide Filter" : "Show Filter"}
                    </Button>
                </Group >
                <hr style={{ width: '30%' }} />
                <Group position='center'>
                    {(!showFilter) ?
                        <></> :
                        <>
                            <Select
                                value={filterTerm}
                                onChange={setFilterTerm}
                                searchable
                                label={"Filter by page frequent terms"}
                                data={termsArray}>
                            </Select>

                            <Select
                                style={{ width: "20%" }}
                                value={sortOption}
                                onChange={setSortOption}
                                label={"Sort By"}
                                data={filterTerm === "" ? sortOptions_noTerm : sortOptions_term}>
                            </Select>

                            <Button
                                onClick={() => {
                                    setAscending(!ascending)
                                }}
                                leftIcon={ascending ? <IconArrowUp height={20} width={20} /> : <IconArrowDown height={20} width={20} />}>
                                {ascending ? "Ascending" : "Descending"}
                            </Button>
                        </>}
                </Group>

                {(filterTerm !== "") ? <><br />Showing <b>{completeFilteredResult.length}</b> filtered results</> : <></>}

                <div
                    style={{
                        marginLeft: "15%",
                        marginRight: "15%",
                        marginTop: "10px"
                    }}>

                    {[...resultInPage].map((item, index) => {
                        return (
                            <ResultItem
                                item={item}
                                key={index}
                                filterTerm={filterTerm} />
                        )
                    })}


                    <br />
                    <Pagination
                        position="center"
                        value={activePage}
                        onChange={setPage}
                        total={(completeFilteredResult.length / 5) + ((completeFilteredResult.length % 5 === 0) ? 0 : 1)} />

                    <br />
                </div>


            </>
        )
    }
}

export default SearchResult;