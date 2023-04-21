import { useState, useEffect } from 'react'
import { Tabs, Text } from '@mantine/core';
import { IconHierarchy2, IconSearch } from '@tabler/icons-react';

import Indexing from './indexing/indexing';
import SearchBar from './search/searchBar'

const TopBar = () => {
    const [activeTab, setActiveTab] = useState('index')

    return (
        <>
            <Tabs value={activeTab} onTabChange={setActiveTab}>
                <Tabs.List grow style={{ fontSize: '30', marginLeft: '20%', marginRight: '20%' }}>
                    <Tabs.Tab value="index" icon={<IconHierarchy2 height={20} width={20} />}><Text>Indexing</Text></Tabs.Tab>
                    <Tabs.Tab value="search" icon={<IconSearch height={20} width={20} />}>Search</Tabs.Tab>
                </Tabs.List>

                <Tabs.Panel value="index" pt="xs">
                    <Indexing
                        activeTab={activeTab} />
                </Tabs.Panel>

                <Tabs.Panel value="search" pt="xs">
                    <SearchBar
                        activeTab={activeTab} />
                </Tabs.Panel>

            </Tabs>
        </>
    );
}

export default TopBar;