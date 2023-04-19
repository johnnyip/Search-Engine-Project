import { useState, useEffect } from 'react'
import { useDisclosure } from '@mantine/hooks';
import { Modal, TextInput, Button, Grid, SegmentedControl, Group } from '@mantine/core';

import SearchResult from './searchResult';
import History from './history';
import Indexes from './indexes';
import { formatDate } from '../../functions/date'

import { queryVector, queryPageRank, querySemantics } from '../../functions/query';
import { getHistoryToken } from '../../functions/cookie'
import { saveRedis, getRedis } from '../../functions/redis'

const SearchBar = () => {
    const [keyword, setKeyword] = useState('')
    const [loading, setLoading] = useState(false)
    const [opened, { open, close }] = useDisclosure(false);
    const [isHistory, setIsHistory] = useState(false)
    const [chosenAlgo, setChosenAlgo] = useState("vector")
    const [queryResult, setQueryResult] = useState({})
    const [history, setHistory] = useState("")

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

        result.queryDate = formatDate(new Date());
        result.algo = chosenAlgo
        setLoading(false)

        //Save cookie

        let historyToken = getHistoryToken()
        let history = await getRedis(historyToken)

        history.unshift(result)
        setHistory(history)

        await saveRedis(historyToken, history)

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

            <Grid style={{ marginLeft: "22%", marginRight: "15%" }}>
                <Grid.Col span={7}>
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

                <Grid.Col span={5}>
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
                            disabled={loading}
                            onClick={() => {
                                open();
                                setIsHistory(true)
                            }}>
                            History
                        </Button>
                        <Button
                            style={{ textAlign: "left" }}
                            disabled={loading}
                            onClick={() => {
                                open();
                                setIsHistory(false)
                            }}>
                            Indexes
                        </Button>

                    </Group>
                </Grid.Col>
            </Grid>


            <br />
            <hr />

            <SearchResult result={queryResult} />

            <Modal
                size="70%"
                opened={opened}
                onClose={close} title={isHistory ? "Search History" : "Indexes"}>

                {(isHistory) ?
                    <History
                        opened={opened}
                        keyword={keyword}
                        setKeyword={setKeyword}
                        onSubmit={onSubmit}
                        close={close} />

                    : <Indexes
                        opened={opened}
                        keyword={keyword}
                        setKeyword={setKeyword}
                        onSubmit={onSubmit}
                        close={close} />
                }
            </Modal>

        </>
    )
}

export default SearchBar;