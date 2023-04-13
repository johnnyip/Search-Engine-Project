import { useState, useEffect } from 'react'
import { Badge, Group } from '@mantine/core';
// import { IconPhoto, IconMessageCircle, IconSettings } from '@tabler/icons';

import { pythonStatus } from './functions/query';
import { javaStatus } from './functions/crawl';

import './style.css'
import TopBar from './components/topBar';

function App() {
  const [python, setPython] = useState(false)
  const [java, setJava] = useState(false)

  useEffect(() => {
    const getStatus = async () => {
      setPython(await pythonStatus())
      setJava(await javaStatus())

    }

    getStatus()
  }, [])
  return (
    <div className="App center" >
      <br />
      <Group position="center" spacing="xl">
        <Badge
          color={python ? "green" : "red"}
          size="lg"
          radius="sm">
          Python Server: <b>{python ? "Connected" : "Not Connected"}</b>
        </Badge>

        <Badge
          color={java ? "green" : "red"}
          size="lg"
          radius="sm">
          Java Server: <b>{java ? "Connected" : "Not Connected"}</b>
        </Badge>
      </Group>

      <h1>Search Engine Project</h1>
      <TopBar />

    </div>
  );
}

export default App;
