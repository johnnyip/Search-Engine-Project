import { useState, useEffect } from 'react'
import { Card, Image, Text, Group } from '@mantine/core';

const ResultItem = (props) => {
    let result = props.item
    console.log(result)

    return (
        <>
            <Card
                withBorder
                radius="md"
                style={{
                    textAlign: "left",
                    marginBottom: "5px"
                }}
                shadow="lg"
                padding="xl"
                component="a"
                href={result.url}
                target="_blank"
            >


                <Group position="apart">
                    <Text weight={500} size="lg" >{result.Title} </Text>
                    <Text fz="xs" color="dimmed" fs="italic">Score: {result.Score}</Text>
                </Group>

                <Group position="apart">
                    <Text fz="xs" color="dimmed" fs="italic">{result.url}</Text>
                    <Text fz="xs" color="dimmed" fs="italic">Page Size: {result["Size of the Page"]} Byte</Text>
                    <Text fz="xs" color="dimmed" fs="italic">Last Modified: {result["Last Modified Date"]}</Text>

                </Group>

                <Text mt="xs" color="dimmed" size="md">
                    Text with keywords <b>bolded</b>
                </Text>
            </Card>


        </>
    )
}

export default ResultItem;