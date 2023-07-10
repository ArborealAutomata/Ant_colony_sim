::: mermaid

graph TD;
    start([Start]);
    load[load];
    id23[[display]]
    id3[refresh]
    id4{quit?};
    id0([Exit]);

    start-->load;
    load-->id23;
    id23-->id3;
    id3-->id4;
    id4-- no--->id23;
    id4-- yes--->id0;
:::