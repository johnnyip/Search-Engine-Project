import { useState, useEffect } from 'react'
import { Pagination } from '@mantine/core';

import ResultItem from './resultItem'

const SearchResult = () => {
    const [activePage, setPage] = useState(1);

    return (
        <>
            <b>100 results (0.51 seconds)</b><br />

            <div
                style={{
                    marginLeft: "15%",
                    marginRight: "15%",
                    marginTop: "10px"
                }}>
                <ResultItem />
                <ResultItem />
                <ResultItem />
                <ResultItem />
                <ResultItem />
                <ResultItem />
                <ResultItem />
                <ResultItem />
                <ResultItem />
                <ResultItem />

                <br />
                <Pagination
                    position="center"
                    value={activePage}
                    onChange={setPage}
                    total={10} />

                <br />
            </div>


        </>
    )
}

export default SearchResult;