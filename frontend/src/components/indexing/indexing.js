import { useState, useEffect } from 'react'
import { TextInput, Button } from '@mantine/core';
import { IconSend } from '@tabler/icons';

import IndexingInfo from './indexingInfo';

const Indexing = () => {
    const [url, setUrl] = useState('')

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
                style={{ marginLeft: "20%", marginRight: "20%" }}
            /><br />

            <Button leftIcon={<IconSend size="1rem" />}>
                Start Crawling
            </Button>

            <IndexingInfo />
        </div >
    )
}


export default Indexing;