USE todo_app;
create table tasks
(
    id           bigint unsigned auto_increment
        primary key,
    created_at   timestamp  default CURRENT_TIMESTAMP null,
    updated_at   timestamp                            null on update CURRENT_TIMESTAMP,
    title        varchar(255)                         not null,
    brief        varchar(255)                         null,
    content      text                                 null,
    is_completed tinyint(1) default 0                 null,
    deadline     datetime(6)                          null,
    user_id      bigint                               not null,
    parent_id    bigint                               null
);

create index idx_user_id
    on tasks (user_id);


