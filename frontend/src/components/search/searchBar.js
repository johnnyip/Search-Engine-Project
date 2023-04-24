import { useState, useEffect } from 'react'
import { useDisclosure } from '@mantine/hooks';
import { Modal, TextInput, Button, Grid, SegmentedControl, Group, Center, Autocomplete } from '@mantine/core';
import { IconSearch, IconHistory, IconSitemap, Icon3dCubeSphere, IconMessageSearch, IconTopologyComplex } from '@tabler/icons-react';

import SearchResult from './searchResult';
import History from './history';
import Indexes from './indexes';
import { formatDate } from '../../functions/date'

import { queryVector, queryPageRank, querySemantics, queryRelated } from '../../functions/query';
import { getHistoryToken } from '../../functions/cookie'
import { saveRedis, getRedis } from '../../functions/redis'
import { getIndexedContent } from '../../functions/crawl'

import { Trie } from '../../functions/keywordSuggestion'

const SearchBar = (props) => {
    let activeTab = props.activeTab

    const [trie, setTrie] = useState(new Trie())
    const [keyword, setKeyword] = useState('')
    const [loading, setLoading] = useState(false)
    const [opened, { open, close }] = useDisclosure(false);
    const [isHistory, setIsHistory] = useState(false)
    const [chosenAlgo, setChosenAlgo] = useState("vector")
    const [queryResult, setQueryResult] = useState({})
    const [history, setHistory] = useState("")

    const [indexMaxTF, setIndexMaxTF] = useState([])
    const [indexStemFreq, setIndexStemFreq] = useState([])
    const [indexRawFreq, setIndexRawFreq] = useState([])
    const [rawContents, setRawContents] = useState({})
    const [historySuggestions, setHistorySuggestions] = useState([])
    const [suggestions, setSuggestions] = useState([])

    let algoOptions = [
        { label: (<Center><Icon3dCubeSphere height={20} width={20} />Vector Space</Center>), value: 'vector' },
        { label: (<Center><IconTopologyComplex height={20} width={20} />PageRank</Center>), value: 'pagerank' },
        { label: (<Center><IconMessageSearch height={20} width={20} />Semantics</Center>), value: 'semantics' }
    ]

    const findKeywords = (keywords) => {
        return trie.searchForSuggestions(keywords)
    }

    const onSubmit = async () => {

        setLoading(true)

        let firstPart = keyword.split(" ")[0].substring(0, 8)

        let result = (firstPart === "related:") ?
            await queryRelated(keyword) :
            (chosenAlgo === "vector") ?
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
        let history_ = await getRedis(historyToken)

        history_.unshift(result)
        setHistory(history_)

        await saveRedis(historyToken, history_)
        loadHistorySuggestions(history_)
    }

    const loadHistorySuggestions = (history_) => {
        let historyQuery = []
        let historyCount = 0
        for (let item of history_) {
            if (!historyQuery.includes(item.data.keyword) && historyCount < 5) {
                historyQuery.push(item.data.keyword)
                historyCount++
            }
        }

        let historySuggestion = []
        // historyQuery.reverse()
        for (let item of historyQuery) {
            historySuggestion.push({ value: item, group: 'Your Last 5 Search History' })
        }

        setSuggestions(historySuggestion)
        setHistorySuggestions(historySuggestion)
    }

    const getSearchHistory = async () => {
        let historyToken = getHistoryToken()
        let history_ = await getRedis(historyToken)
        setHistory(history_)
        loadHistorySuggestions(history_)
    }

    const getIndexes = async () => {
        const indexStat_ = await getIndexedContent();
        console.log(indexStat_)
        setIndexMaxTF(indexStat_.maxTFList !== undefined ? indexStat_.maxTFList : [])
        setIndexStemFreq(indexStat_.stemFrequencies !== undefined ? indexStat_.stemFrequencies : [])

        let rawIndex = indexStat_.rawFrequencies !== undefined ? indexStat_.rawFrequencies : []
        setIndexRawFreq(rawIndex)

        let rawContents = indexStat_.rawContentMap !== undefined ? indexStat_.rawContentMap : {}
        setRawContents(rawContents)

        //Init the keyword suggestion tree
        for (let item of rawIndex) {
            trie.insert(item.stem)
        }

        // console.log(trie.searchForSuggestions("am"))

    }
    useEffect(() => {
        if (activeTab === "search") {
            getIndexes()
            getSearchHistory()
        }
    }, [activeTab])


    return (
        <>
            <Group position='center'>
                <h4>Searching Algorithm</h4>

                <SegmentedControl fullWidth
                    value={chosenAlgo}
                    onChange={setChosenAlgo}
                    data={algoOptions}
                />

                <Button
                    leftIcon={<IconHistory height={20} width={20} />}
                    style={{ textAlign: "left" }}
                    disabled={loading}
                    onClick={() => {
                        open();
                        setIsHistory(true)
                    }}>
                    History
                </Button>
                <Button
                    leftIcon={<IconSitemap height={20} width={20} />}
                    style={{ textAlign: "left" }}
                    disabled={loading}
                    onClick={() => {
                        open();
                        setIsHistory(false)
                    }}>
                    Indexes
                </Button>

            </Group>

            <h3>Enter Search Keyword</h3>

            <Grid style={{ marginLeft: "28%", marginRight: "15%" }}>
                <Grid.Col span={8}>
                    <Autocomplete
                        value={keyword}
                        onChange={(e) => {
                            setKeyword(e)
                            let suggestion = []
                            //add historySuggestions to the suggestion
                            suggestion = suggestion.concat(historySuggestions)

                            if (e.length > 0) {
                                let keyword_ = e
                                let words = keyword_.split(' ')
                                let firstWords = words.slice(0, words.length - 1).join(' ')
                                let lastWord = words[words.length - 1]
                                let suggestedList = findKeywords(lastWord)
                                if (lastWord !== "") {
                                    for (let item of suggestedList) {
                                        suggestion.push({ value: `${firstWords} ${item}`, group: 'Suggested Keywords' })
                                    }
                                }
                            }

                            // console.log(historySuggestions)
                            // suggestion = suggestion.concat(historySuggestions)
                            console.log(suggestion)
                            setSuggestions(suggestion)


                        }}
                        icon={<IconSearch height={20} width={20} />}
                        data={suggestions}
                        onKeyDown={(e) => {
                            if (e.key === 'Enter') {
                                onSubmit();
                            }
                        }}
                    />

                </Grid.Col>

                <Grid.Col span={2}>
                    <Group position="left" spacing="xs">
                        <Button
                            leftIcon={<IconSearch height={20} width={20} />}
                            disabled={keyword.length === 0}
                            style={{ textAlign: "left" }}
                            loading={loading}
                            onClick={async (e) => {
                                e.preventDefault();
                                await onSubmit()
                            }}>
                            Search
                        </Button>
                    </Group>
                </Grid.Col>
            </Grid>


            <br />
            <hr />

            <SearchResult
                result={queryResult}
                rawContents={rawContents} />

            <Modal
                size="70%"
                opened={opened}
                onClose={close} title={isHistory ? "Search History" : "Indexes"}>

                {(isHistory) ?
                    <History
                        rawContents={rawContents}
                        history={history}
                        setHistory={setHistory}
                        opened={opened}
                        keyword={keyword}
                        setKeyword={setKeyword}
                        onSubmit={onSubmit}
                        close={close} />

                    : <Indexes
                        indexMaxTF={indexMaxTF}
                        indexRawFreq={indexRawFreq}
                        indexStemFreq={indexStemFreq}
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