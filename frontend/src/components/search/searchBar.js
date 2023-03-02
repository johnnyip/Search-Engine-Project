import { useState, useEffect } from 'react'
import { TextInput, Button, Grid } from '@mantine/core';

import SearchResult from './searchResult';

const SearchBar = () => {
    const [keyword, setKeyword] = useState('')

    return (
        <>
            <h3>Enter Search Keyword</h3>

            <Grid style={{ marginLeft: "30%", marginRight: "30%" }}>
                <Grid.Col span={11}>
                    <TextInput
                        value={keyword}
                        onChange={(event) => setKeyword(event.currentTarget.value)}
                    />
                </Grid.Col>

                <Grid.Col span={1}>
                    <Button style={{ textAlign: "left" }}>Search</Button>
                </Grid.Col>
            </Grid>


            <br />
            <hr />
            <div
                style={{
                    backgroundColor: "#F7F7F7",
                    borderRadius: 20
                }}>

                <SearchResult />
            </div>

        </>
    )
}

export default SearchBar;