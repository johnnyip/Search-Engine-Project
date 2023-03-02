import { useState, useEffect } from 'react'
import { Card, Image, Text } from '@mantine/core';

const ResultItem = () => {
    return (
        <>
            <Card
                radius="md"
                style={{
                    textAlign: "left",
                    // padding: 20
                }}
                shadow="lg"
                padding="xl"
                component="a"
                href="https://www.youtube.com/watch?v=dQw4w9WgXcQ"
                target="_blank"
            >

                <Text weight={500} size="lg" mt="md">
                    Result Title
                </Text>

                <Text fz="xs" color="dimmed" fs="italic">
                    https://www.cse.ust.hk/~kwtleung/COMP4321/Movie/278.html
                </Text>

                <Text mt="xs" color="dimmed" size="md">
                    Text with keywords <b>bolded</b>
                </Text>
            </Card>

            <br />

        </>
    )
}

export default ResultItem;