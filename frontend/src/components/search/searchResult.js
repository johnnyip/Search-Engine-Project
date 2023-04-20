import { useState, useEffect } from 'react'
import { Pagination, Select, Group, Button } from '@mantine/core';

import ResultItem from './resultItem'

const SearchResult = (props) => {
    let result = props.result
    const itemPerPage = 5;

    const [activePage, setPage] = useState(1);
    const [resultInPage, setResultInPage] = useState([])
    const [completeFilteredResult, setCompleteFilteredResult] = useState([])

    const [showFilter, setShowFilter] = useState(false)
    const [filterTerm, setFilterTerm] = useState("")
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
            console.log(uniqueTermsArray)
            setTermsArray(uniqueTermsArray)
        }
    }

    const extractResultInPage = async () => {
        let result_ = []
        if (filterTerm === "") {
            result_ = result.data.result
        } else {
            for (let item of result.data.result) {
                if (item["Most Frequent Items"].map((item) => item.Item).indexOf(filterTerm) !== -1) {
                    result_.push(item)
                }
            }
        }
        setCompleteFilteredResult(result_)
        pagination(result_)

    }

    const pagination = (result_) => {
        console.log("result_")
        console.log(result_)
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
        console.log(result)
        if (Object.keys(result).length !== 0) {
            setFilterTerm("")
            extractResultInPage()
        }
        extractDocumentTerms()
    }, [result])

    useEffect(() => {
        if (Object.keys(result).length !== 0) {
            extractResultInPage()
        }
    }, [filterTerm])

    useEffect(() => {
        pagination()
    }, [activePage])

    if (Object.keys(result).length !== 0) {
        return (
            <>
                <Group position='center'>
                    <b>{result.data.result.length} results ({result.data.time})</b>
                    <Button
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
                                style={{ width: '23%' }}
                                searchable
                                placeholder='Term(# of occurence in retrieved document)'
                                label={"Filter by page frequent terms"}
                                data={termsArray}>
                            </Select>

                        </>}
                </Group>

                {(showFilter) ? <><br />Showing <b>{completeFilteredResult.length}</b> filtered results</> : <></>}

                <div
                    style={{
                        marginLeft: "15%",
                        marginRight: "15%",
                        marginTop: "10px"
                    }}>

                    {[...resultInPage].map((item, index) => {
                        return (
                            <ResultItem item={item} key={index} />
                        )
                    })}


                    <br />
                    <Pagination
                        position="center"
                        value={activePage}
                        onChange={setPage}
                        total={(completeFilteredResult.length / 5) + 1} />

                    <br />
                </div>


            </>
        )
    }
}

export default SearchResult;