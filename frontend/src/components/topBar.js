import { useState, useEffect } from 'react'
import { Tabs } from '@mantine/core';
import { IconHierarchy2, IconSearch } from '@tabler/icons';

const TopBar = () => {
    const [activeTab, setActiveTab] = useState('index')

    return (
        <>
            <Tabs variant="outline" value={activeTab} onTabChange={setActiveTab}>
                <Tabs.List grow style={{fontSize: '30'}}> 
                    <Tabs.Tab value="index" icon={<IconHierarchy2 size={14} />}>Indexing</Tabs.Tab>
                    <Tabs.Tab value="search" icon={<IconSearch size={14} />}>Search</Tabs.Tab>
                </Tabs.List>

                <Tabs.Panel value="index" pt="xs">
                    Indexing Page
                </Tabs.Panel>

                <Tabs.Panel value="search" pt="xs">
                    Messages tab content
                </Tabs.Panel>

            </Tabs>
        </>
    );
}

export default TopBar;