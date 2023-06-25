::: mermaid

graph TD;
    start([Start]);
    load[[Load]];
    sprite[pygame \n sprite];
    ant[Ants];
    food[Food];
    wall[Wall];
    nest[Nest];
    pher[Pheromone];
    attr[Attract \n Pheromone];
    repl[Repel \n Pheromone]
    main[[MAINLOOP]]
    que{quit?};
    exit([Exit]);

    start-->load;
    load-->sprite;
    sprite-->ant;
    sprite-->food;
    sprite-->wall;
    sprite-->nest;
    sprite-->pher;
    pher-->attr;
    pher-->repl;
    load-->main;
    main-->que;
    que-- no--->main;
    que-- yes--->exit;
:::