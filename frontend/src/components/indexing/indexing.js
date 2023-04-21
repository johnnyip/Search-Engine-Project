import { useState, useEffect } from 'react'
import { TextInput, Button, Group, Stepper } from '@mantine/core';
import { IconSend, IconTrash } from '@tabler/icons-react';

import IndexingInfo from './indexingInfo';

import { checkIndexStat, startCrawl, updateIndex, removeCrawlContent } from '../../functions/crawl'
import { dbUpdate } from '../../functions/query'

const Indexing = (props) => {
    let activeTab = props.activeTab

    const [url, setUrl] = useState('https://www.cse.ust.hk/~kwtleung/COMP4321/testpage.htm')
    const [loading, setLoading] = useState(false)
    const [loading2, setLoading2] = useState(false)
    const [indexStat, setIndexStat] = useState({})
    const [timeElapsed, setTimeElapsed] = useState(0)
    const [active, setActive] = useState(0);
    const [busy, setBusy] = useState(false);

    function timeout(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    const startTimer = (stopCallback) => {
        setTimeElapsed(0);
        const duration = setInterval(() => {
            setTimeElapsed(timeElapsed => timeElapsed + 1);
        }, 1000);

        // Call stopCallback to stop the timer
        const stopTimer = () => {
            clearInterval(duration);
            stopCallback();
        };

        // Return stopTimer function
        return stopTimer;
    };

    const loadData = async () => {
        const indexStat_ = await checkIndexStat()
        setIndexStat(indexStat_)
        console.log(indexStat_)
        if (indexStat_.totalPageCrawled !== 0) {
            setActive(3)
        }
    }

    const crawl = async (fake) => {
        let timerStopped = false;
        const stopTimerCallback = () => {
            timerStopped = true;
        };
        const stopTimer = startTimer(stopTimerCallback);
        if (!fake) {
            let stat
            if (indexStat.totalPageCrawled === 0) {
                stat = await startCrawl(url);
            } else {
                stat = await updateIndex(url);
            }
            setIndexStat(stat)
        } else {
            console.log("fake")
            await timeout(5000);
        }
        if (!timerStopped) {
            stopTimer();
        }
    }

    const sync = async (fake) => {
        setTimeElapsed(0);
        let timerStopped = false;
        const stopTimerCallback = () => {
            timerStopped = true;
        };
        const stopTimer = startTimer(stopTimerCallback);
        if (!fake) {
            await dbUpdate();
        } else {
            console.log("fake")
            await timeout(5000);
        }
        if (!timerStopped) {
            stopTimer();
        }
    }

    useEffect(() => {
        if (activeTab === "index") {
            console.log("Indexing page loaded")
            loadData()
        }
    }, [activeTab])


    return (
        <div className='moreSpace'>
            <h3>Enter the URL to be crawled</h3>
            <Button
                color="gray"
                onClick={() => setUrl("https://www.cse.ust.hk/~kwtleung/COMP4321/testpage.htm")}
                style={{ margin: 10 }}>
                Load sample data URL
            </Button>

            <TextInput
                value={url}
                onChange={(event) => setUrl(event.currentTarget.value)}
                disabled
                style={{ marginLeft: "20%", marginRight: "20%" }}
            /><br />

            {(!busy) ? <Group position="center">
                <Button
                    color="red"
                    disabled={indexStat.totalPageCrawled === undefined && indexStat.totalPageCrawled === 0 || loading || loading2}
                    onClick={async () => {
                        setLoading(true)
                        let stat = await removeCrawlContent()
                        setIndexStat(stat)
                        setLoading(false)
                    }}
                    leftIcon={<IconTrash height={20} width={20} />}>
                    Remove All Indexing
                </Button>

                <Button
                    loading={loading}
                    disabled={loading2}
                    onClick={async () => {
                        setBusy(true)
                        setActive(1)
                        await crawl(false)
                        setActive(2)
                        await sync(false)
                        setActive(3)
                        setBusy(false)
                    }}
                    leftIcon={<IconSend height={20} width={20} />}>
                    Submit URL and {(indexStat.totalPageCrawled !== 0) ? "Update Index" : "Build Index"}
                </Button>

                {/* <Button
                    loading={loading2}
                    disabled={loading}
                    onClick={async () => {
                    }}
                    leftIcon={<IconSend height={20} width={20} />}>
                    {(loading2) ? `Sync Database...(${timeElapsed}s)` : "Sync Database (Python)"}
                </Button> */}
            </Group>
                : <></>}

            <br /><br />

            <Stepper
                style={{ marginLeft: "20%", marginRight: "20%" }}
                active={active}
                onStepClick={async (e) => {
                    setActive(e)
                    if (e === 1) {
                        await crawl(true)
                        setActive(2)
                        await sync(true)
                        setActive(3)
                    }
                    else if (e === 2) {
                        await sync(false)
                        setActive(3)
                    }

                }}
                breakpoint="sm">
                <Stepper.Step
                    label="Enter URL"
                    description="Submit URL to backend">
                    Step 1: Enter URL, submit to backend to start process
                </Stepper.Step>
                <Stepper.Step
                    loading={active === 1}
                    label={`Crawling and ${(indexStat.totalPageCrawled !== 0) ? "Updating Index" : "Building Index"} ${active === 1 ? `(${timeElapsed}s)` : ""}`}
                    description={`[Java] Crawl and ${(indexStat.totalPageCrawled !== 0) ? "Updating the Existing Index" : "Building Index For the First Time"}`}>
                    Step 2: Java Server is crawling and
                    {(indexStat.totalPageCrawled !== 0) ? "updating the index" : "building the index"}
                    with the webpages content, then store result to SQLite...
                </Stepper.Step>
                <Stepper.Step
                    loading={active === 2}
                    label={`Data Synchronization ${active === 2 ? `(${timeElapsed}s)` : ""}`}
                    description="[Python] Sync Data and Get Ready">
                    Step 3: Python Server is syncing data...
                </Stepper.Step>
                <Stepper.Completed>
                    Indexing completed, ready to be searched
                </Stepper.Completed>
            </Stepper>



            <IndexingInfo indexStat={indexStat} />
        </div>
    )


}


export default Indexing;