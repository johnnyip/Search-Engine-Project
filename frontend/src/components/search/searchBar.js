import { useState, useEffect } from 'react'
import { useDisclosure } from '@mantine/hooks';
import { Modal, TextInput, Button, Grid, SegmentedControl, Group } from '@mantine/core';

import SearchResult from './searchResult';
import History from './history';
import { formatDate } from '../../functions/date'

import { queryVector, queryPageRank, querySemantics } from '../../functions/query';
import { saveHistory, getHistory } from '../../functions/cookie'

const SearchBar = () => {
    const [keyword, setKeyword] = useState('')
    const [loading, setLoading] = useState(false)
    const [opened, { open, close }] = useDisclosure(false);
    const [chosenAlgo, setChosenAlgo] = useState("vector")
    const [queryResult, setQueryResult] = useState({})
    const [cookie, setCookie] = useState("")

    let algoOptions = [
        { label: 'Vector Space', value: 'vector' },
        { label: 'PageRank', value: 'pagerank' },
        { label: 'Semantics Search', value: 'semantics' },
    ]

    const onSubmit = async () => {

        setLoading(true)

        let result = (chosenAlgo === "vector") ?
            await queryVector(keyword) :
            (chosenAlgo === "pagerank") ?
                await queryPageRank(keyword) :
                await querySemantics(keyword)
        setQueryResult(result)
        console.log(result)

        result.queryDate = formatDate(new Date());
        result.algo = chosenAlgo
        setLoading(false)

        //Save cookie

        let history = getHistory()
        history.unshift(result)
        let historyString = JSON.stringify(history)
        saveHistory(historyString)
        setCookie(history)
        console.log(history)

    }

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

            <Grid style={{ marginLeft: "25%", marginRight: "15%" }}>
                <Grid.Col span={8}>
                    <TextInput
                        value={keyword}
                        onKeyDown={(e) => {
                            if (e.key === 'Enter') {
                                onSubmit();
                            }
                        }}
                        onChange={(event) => setKeyword(event.currentTarget.value)}
                    />
                </Grid.Col>

                <Grid.Col span={4}>
                    <Group position="left" spacing="xs">
                        <Button
                            disabled={keyword.length === 0}
                            style={{ textAlign: "left" }}
                            loading={loading}
                            onClick={async (e) => {
                                e.preventDefault();
                                await onSubmit()
                            }}>
                            Search
                        </Button>
                        <Button
                            style={{ textAlign: "left" }}
                            loading={loading}
                            onClick={open}>
                            History
                        </Button>

                    </Group>
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

            <Modal
                size="70%"
                opened={opened}
                onClose={close} title="Search History">

                <History
                    keyword={keyword}
                    setKeyword={setKeyword}
                    onSubmit={onSubmit}
                    close={close} />
            </Modal>

        </>
    )
}

export default SearchBar;