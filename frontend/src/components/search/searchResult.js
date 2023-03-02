import { useState, useEffect } from 'react'

import ResultItem from './resultItem'

const SearchResult = () => {
    return (
        <>
            <b>100 results (0.51 seconds)</b>

            <div
                style={{
                    marginLeft: "15%",
                    marginRight: "15%",
                }}>
                <ResultItem />

                <ResultItem />
            </div>
        </>
    )
}

export default SearchResult;