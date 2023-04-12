import { useState, useEffect } from 'react'
import { Pagination } from '@mantine/core';

import ResultItem from './resultItem'

const SearchResult = (props) => {
    let result = props.result

    const [activePage, setPage] = useState(1);

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

                    {[...result.data.result].map((item, index) => {
                        return (
                            <ResultItem item={item} key={index} />
                        )
                    })}


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
}

export default SearchResult;