import { useState, useEffect } from 'react'
import { Button, Group, TextInput, Grid, SegmentedControl, Table, Pagination } from '@mantine/core';
import { IconX, IconPlus, IconArrowUp, IconArrowDown } from '@tabler/icons';

import { checkIndexStat } from '../../functions/crawl'

const Indexes = (props) => {
    let opened = props.opened
    let close = props.close
    let keyword = props.keyword
    let setKeyword = props.setKeyword
    let onSubmit = props.onSubmit

    const itemPerPage = 20;

    const [indexStat, setIndexStat] = useState({})
    const [searchFilter, setSearchFilter] = useState("")
    const [filteredItems, setFilteredItems] = useState([])
    const [ascending, setAscending] = useState(true)
    const [maxTF, setMaxTF] = useState([])
    const [stemmedWord, setStemmedWord] = useState([])
    const [resultInPage, setResultInPage] = useState([])
    const [activePage, setActivePage] = useState(1)

    const [chosenTab, setChosenTab] = useState("maxtf")
    let tabOptions = [
        { label: 'Max TF of document', value: 'maxtf' },
        { label: 'Stemmed Word Frequency', value: 'stem' }

    ]


    const loadData = async () => {
        const indexStat_ = await checkIndexStat()
        setIndexStat(indexStat_)
        let maxTF_ = indexStat_.maxTFList !== undefined ? indexStat_.maxTFList : []
        let stemmedWord_ = indexStat_.stemFrequencies !== undefined ? indexStat_.stemFrequencies : []

        // Sort
        maxTF_.sort((a, b) => { return !ascending ? b.frequency - a.frequency : a.frequency - b.frequency })
        stemmedWord_.sort((a, b) => { return !ascending ? b.frequency - a.frequency : a.frequency - b.frequency })

        setMaxTF(maxTF_)
        setStemmedWord(stemmedWord_)
    }

    const filterItem = () => {
        if ((chosenTab == "maxtf" && maxTF.length !== 0) ||
            chosenTab == "stem" && stemmedWord.length !== 0) {
            let start = (activePage - 1) * itemPerPage;
            let end = start + itemPerPage;

            let dataInPage = []
            //Apply filter
            if (searchFilter == "") {
                dataInPage = chosenTab == "maxtf" ? maxTF : stemmedWord
            } else if (chosenTab == "maxtf") {
                dataInPage = maxTF.filter((item) => {
                    return item.title !== undefined && item.title.toLowerCase().includes(searchFilter.toLowerCase())
                })
            } else {
                dataInPage = stemmedWord.filter((item) => {
                    return item.stem !== undefined && item.stem.toLowerCase().includes(searchFilter.toLowerCase())
                })
            }
            setFilteredItems(dataInPage)

            if (dataInPage.length > 0) {
                dataInPage = chosenTab == "maxtf" ? dataInPage.slice(start, end) : dataInPage.slice(start, end)
            }

            // setFilteredItems(dataInPage)
            setResultInPage(dataInPage)
            console.log(dataInPage)
        }
    }

    useEffect(() => {
        filterItem()
    }, [searchFilter, maxTF, stemmedWord, activePage, ascending])

    useEffect(() => {
        setSearchFilter("")
        filterItem()
    }, [chosenTab])

    useEffect(() => {
        // console.log("Indexing page loaded")
        loadData()
        filterItem()
    }, [opened])


    return (
        <>
            <div>Current Search</div>
            <Grid style={{ marginLeft: "15%", marginRight: "0%" }}>

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
                            onClick={() => {
                                setKeyword("")
                            }}
                            leftIcon={<IconX size="15" />}>
                            Clear
                        </Button>
                        <Button
                            disabled={keyword.length === 0}
                            style={{ textAlign: "left" }}
                            onClick={async (e) => {
                                e.preventDefault();
                                close()
                                await onSubmit()
                            }}>
                            Search
                        </Button>

                    </Group>
                </Grid.Col>
            </Grid>
            <hr />
            <div style={{ paddingLeft: "5%", paddingRight: "5%" }}>

                <SegmentedControl
                    fullWidth
                    value={chosenTab}
                    onChange={setChosenTab}
                    data={tabOptions}
                />
            </div>
            <br />
            <br />



            <div style={{ paddingLeft: "15%", paddingRight: "15%" }}>

                {/* Sort button */}
                <Grid>
                    <Grid.Col span={10}>
                        <TextInput
                            placeholder='Filter '
                            value={searchFilter}
                            onChange={(event) => {
                                setSearchFilter(event.currentTarget.value)
                            }}
                        />
                    </Grid.Col>
                    <Grid.Col span={2}>
                        <Button
                            onClick={() => {
                                setAscending(!ascending)
                                setMaxTF(maxTF.sort((a, b) => { return ascending ? b.frequency - a.frequency : a.frequency - b.frequency }))
                                setStemmedWord(stemmedWord.sort((a, b) => { return ascending ? b.count - a.count : a.count - b.count }))
                            }}
                            leftIcon={ascending ? <IconArrowUp size={20} /> : <IconArrowDown size={20} />}>
                            {ascending ? "Ascending" : "Descending"}
                        </Button>
                    </Grid.Col>
                </Grid>

                <h2>{filteredItems.length} Results</h2>

                {chosenTab === "maxtf" ?

                    // Max TF table
                    <Table striped highlightOnHover withBorder withColumnBorders>
                        <thead>
                            <td style={{ textAlign: "center" }}>Title</td>
                            <td style={{ textAlign: "center" }}>MaxTF</td>
                        </thead>
                        <tbody>
                            {resultInPage.map((item, index) => {
                                return (
                                    <tr key={index}>
                                        <td>{item.title}</td>
                                        <td>{item.frequency}</td>
                                    </tr>
                                )
                            })}
                        </tbody>
                    </Table> :
                    <Table striped highlightOnHover withBorder withColumnBorders>
                        <thead>
                            <td style={{ textAlign: "center" }}>Stemmed word</td>
                            <td style={{ textAlign: "center" }}>Frequency</td>
                            <td style={{ textAlign: "center" }}>Action</td>
                        </thead>
                        <tbody>
                            {resultInPage.map((item, index) => {
                                return (
                                    <tr key={index}>
                                        <td>{item.stem}</td>
                                        <td>{item.count}</td>
                                        <td style={{ textAlign: "center", width:"20%" }}>
                                            <Button
                                                onClick={() => {
                                                    setKeyword(`${keyword} ${item.stem}`)
                                                }}
                                                leftIcon={<IconPlus size={20} />}>
                                                Append keyword
                                            </Button>
                                        </td>
                                    </tr>
                                )
                            })}
                        </tbody>
                    </Table>}
                <Pagination
                    position="center"
                    value={activePage}
                    onChange={setActivePage}
                    total={(filteredItems.length / itemPerPage) + 1} />

            </div>
        </>
    )
}

export default Indexes;