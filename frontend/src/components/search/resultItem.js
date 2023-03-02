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

                <Text mt="xs" color="dimmed" size="sm">
                    Text with keywords bolded
                </Text>
            </Card>

            <br />

        </>
    )
}

export default ResultItem;