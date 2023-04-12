import { useState, useEffect } from 'react'
import { TextInput, Button, Grid, SegmentedControl, Group } from '@mantine/core';

import SearchResult from './searchResult';

import { queryVector, queryPageRank, querySemantics } from '../../functions/query';

const SearchBar = () => {
    const [keyword, setKeyword] = useState('MOvie "dinosaur" imDB hkust admission ug')
    const [loading, setLoading] = useState(false)
    const [chosenAlgo, setChosenAlgo] = useState("vector")
    const [queryResult, setQueryResult] = useState({})

    let algoOptions = [
        { label: 'Vector Space', value: 'vector' },
        { label: 'PageRank', value: 'pagerank' },
        { label: 'Semantics Search', value: 'semantics' },
    ]


    return (
        <>
            <Group position='center'>
                <h4>Searching Algorithm</h4>

                <SegmentedControl fullWidth
                    value={chosenAlgo}
                    onChange={setChosenAlgo}
                    data={algoOptions}
                />
            </Group>

            <h3>Enter Search Keyword</h3>

            <Grid style={{ marginLeft: "30%", marginRight: "30%" }}>
                <Grid.Col span={11}>
                    <TextInput
                        value={keyword}
                        onChange={(event) => setKeyword(event.currentTarget.value)}
                    />
                </Grid.Col>

                <Grid.Col span={1}>
                    <Button
                        disabled={keyword.length === 0}
                        style={{ textAlign: "left" }}
                        loading={loading}
                        onClick={async () => {
                            setLoading(true)

                            let result = (chosenAlgo === "vector") ?
                                await queryVector(keyword) :
                                (chosenAlgo === "pagerank") ?
                                    await queryPageRank(keyword) :
                                    await querySemantics(keyword)
                            setQueryResult(result)
                            console.log(result)

                            setLoading(false)
                        }}>
                        Search
                    </Button>
                </Grid.Col>
            </Grid>


            <br />
            <hr />
            <div
                style={{
                    backgroundColor: "#F7F7F7",
                    borderRadius: 20
                }}>

                <SearchResult result={queryResult} />
            </div>

        </>
    )
}

export default SearchBar;