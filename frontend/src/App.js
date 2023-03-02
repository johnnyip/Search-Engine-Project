import { useState, useEffect } from 'react'
import { Tabs } from '@mantine/core';
import { IconPhoto, IconMessageCircle, IconSettings } from '@tabler/icons';

import './style.css'
import TopBar from './components/topBar';

function App() {
  return (
    <div className="App center" >

      <h1>Search Engine Project</h1>
      <TopBar />

    </div>
  );
}

export default App;
