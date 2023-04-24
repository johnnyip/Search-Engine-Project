import { useState, useEffect } from 'react'
import { Button, Group, TextInput, Grid, SegmentedControl, Table, Pagination } from '@mantine/core';
import { IconX, IconPlus, IconArrowUp, IconArrowDown, IconSearch } from '@tabler/icons-react';

// import { getIndexedContent } from '../../functions/crawl'

const Indexes = (props) => {
    let opened = props.opened
    let close = props.close
    let keyword = props.keyword
    let setKeyword = props.setKeyword
    let onSubmit = props.onSubmit
    let indexMaxTF = props.indexMaxTF
    let indexStemFreq = props.indexStemFreq
    let indexRawFreq = props.indexRawFreq

    const itemPerPage = 20;

    const [searchFilter, setSearchFilter] = useState("")
    const [filteredItems, setFilteredItems] = useState([])
    const [ascending, setAscending] = useState(false)
    const [maxTF, setMaxTF] = useState([])
    const [stemmedWord, setStemmedWord] = useState([])
    const [rawWord, setRawWord] = useState([])
    const [resultInPage, setResultInPage] = useState([])
    const [activePage, setActivePage] = useState(1)

    const [chosenTab, setChosenTab] = useState("maxtf")
    let tabOptions = [
        { label: 'Max TF of document', value: 'maxtf' },
        { label: 'Stemmed Word Frequency', value: 'stem' },
        { label: 'Raw Word Frequency', value: 'raw' }

    ]

    const sortDataByFrequency = (data) => {
        const sortKey = data[0]?.count !== undefined ? 'count' : 'frequency';
        return data.sort((a, b) => (ascending ? a[sortKey] - b[sortKey] : b[sortKey] - a[sortKey]));
    };


    const filterItem = () => {
        if ((chosenTab === "maxtf" && maxTF.length !== 0) ||
            (chosenTab === "stem" && stemmedWord.length !== 0) ||
            (chosenTab === "raw" && rawWord.length !== 0)) {
            let start = (activePage - 1) * itemPerPage;
            let end = start + itemPerPage;

            let dataInPage = []
            //Apply filter
            if (searchFilter === "") {
                dataInPage = chosenTab === "maxtf" ? maxTF : chosenTab === "stem" ? stemmedWord : rawWord
            } else if (chosenTab === "maxtf") {
                dataInPage = maxTF.filter((item) => {
                    return item.title !== undefined && item.title.toLowerCase().includes(searchFilter.toLowerCase())
                })
            } else if (chosenTab === "stem") {
                dataInPage = stemmedWord.filter((item) => {
                    return item.stem !== undefined && item.stem.toLowerCase().includes(searchFilter.toLowerCase())
                })
            } else {
                dataInPage = rawWord.filter((item) => {
                    return item.stem !== undefined && item.stem.toLowerCase().includes(searchFilter.toLowerCase())
                })
            }

            // Sort data after filtering
            dataInPage = sortDataByFrequency(dataInPage);

            setFilteredItems(dataInPage)



            if (dataInPage.length > 0) {
                dataInPage = dataInPage.slice(start, end)
            }


            // setFilteredItems(dataInPage)
            setResultInPage(dataInPage)
            // console.log(dataInPage)
        }
    }

    useEffect(() => {
        filterItem()
    }, [searchFilter, maxTF, stemmedWord, rawWord, activePage, ascending, chosenTab])

    useEffect(() => {
        setMaxTF(indexMaxTF)
        setStemmedWord(indexStemFreq)
        setRawWord(indexRawFreq)
    }, [opened]);

    return (
        <>
            <div>Current Search</div>
            <Grid style={{ marginLeft: "15%", marginRight: "0%" }}>

                <Grid.Col span={8}>
                    <TextInput
                        value={keyword}
                        onKeyDown={(e) => {
                            if (e.key === 'Enter') {
                                onSubmit(keyword);
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
                            leftIcon={<IconX height={20} width={20} />}>
                            Clear
                        </Button>
                        <Button
                            leftIcon={<IconSearch height={20} width={20} />}
                            disabled={keyword.length === 0}
                            style={{ textAlign: "left" }}
                            onClick={async (e) => {
                                e.preventDefault();
                                close()
                                await onSubmit(keyword)
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


            <div style={{ paddingLeft: "15%", paddingRight: "15%" }}>

                {/* Sort button */}
                <h3>Search from Indexes</h3>
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
                                setAscending(!ascending);
                            }}
                            leftIcon={ascending ? <IconArrowUp height={20} width={20} /> : <IconArrowDown height={20} width={20} />}>
                            {ascending ? "Ascending" : "Descending"}
                        </Button>
                    </Grid.Col>
                </Grid>

                <h3>{filteredItems.length} Results</h3>

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
                    chosenTab === "stem" ?
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
                                            <td style={{ textAlign: "center" }}>{item.stem}</td>
                                            <td style={{ textAlign: "center" }}>{item.count}</td>
                                            <td style={{ textAlign: "center", width: "20%" }}>
                                                <Button
                                                    onClick={() => {
                                                        setKeyword(`${keyword} ${item.stem}`)
                                                    }}
                                                    leftIcon={<IconPlus height={20} width={20} />}>
                                                    Append keyword
                                                </Button>
                                            </td>
                                        </tr>
                                    )
                                })}
                            </tbody>
                        </Table> :
                        <Table striped highlightOnHover withBorder withColumnBorders>
                            <thead>
                                <td style={{ textAlign: "center" }}>Raw word</td>
                                <td style={{ textAlign: "center" }}>Frequency</td>
                                <td style={{ textAlign: "center" }}>Action</td>
                            </thead>
                            <tbody>
                                {resultInPage.map((item, index) => {
                                    return (
                                        <tr key={index}>
                                            <td style={{ textAlign: "center" }}>{item.stem}</td>
                                            <td style={{ textAlign: "center" }}>{item.count}</td>
                                            <td style={{ textAlign: "center", width: "20%" }}>
                                                <Button
                                                    onClick={() => {
                                                        setKeyword(`${keyword} ${item.stem}`)
                                                    }}
                                                    leftIcon={<IconPlus height={20} width={20} />}>
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