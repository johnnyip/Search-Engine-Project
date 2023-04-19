import { useState, useEffect } from 'react'
import { Pagination } from '@mantine/core';

import ResultItem from './resultItem'

const SearchResult = (props) => {
    let result = props.result
    const itemPerPage = 5;

    const [activePage, setPage] = useState(1);
    const [resultInPage, setResultInPage] = useState([])

    useEffect(() => {
        if (Object.keys(result).length !== 0) {
            let start = (activePage - 1) * itemPerPage;
            let end = start + itemPerPage;
            let dataInPage = result.data.result.slice(start, end)
            setResultInPage(dataInPage)
        }

    }, [result, activePage])

    if (Object.keys(result).length !== 0) {
        return (
            <>
                <b>{result.data.result.length} results ({result.data.time})</b><br />

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
                        total={(result.data.result.length / 5)} />

                    <br />
                </div>


            </>
        )
    }
}

export default SearchResult;