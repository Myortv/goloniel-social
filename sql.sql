create table user_profile(
	-- local user profile for social db
	id serial primary key,
	real_id bigint
	-- user id getted from outside of db
);


create table master (
	id serial primary key,
	user_profile_id int references user_profile(id) on delete cascade not null unique,
	is_approved boolean not null default false,

	title text not null,
	description text,
	cover_picture text
);

with profile as (
	select
		master.id as master_id
    from
		user_profile 
    left join
		master
    on
		master.user_profile_id = user_profile.id
    where
		user_profile.real_id = $1 
)
select
	*
from
	master_approvals
where
	master_id = (select master_id form profile)
;

with user_profile as (
	select
		*
	from
		user_profile
	where
		real_id = $1
)
insert into
	master (user_profile_id, title)
	values (
		user_profile.id,
		$2
	-- "")""

create view view_profile as 
select
	user_profile.id user_profile_id,
	user_profile.real_id real_id,
	master.id master_id
from
	user_profile
left join
	master
on
	master.user_profile_id = user_profile.id
;

create view view_master as
	with agg_master_approvals as (
		select
			count(user_profile_id) as approvals_amount,
			master_id
		from
			master_approvals
		group by
			master_approvals.master_id
	),
	avg_master_rating as (
		select
			avg(rating) as rating,
			master_id
		from
			master_rating
		group by
			master_rating.master_id
	)
	select
		master.*,
		user_profile.real_id as user_real_id,
		agg_master_approvals.approvals_amount,
		avg_master_rating.rating
	from
		master
	left join
		user_profile
	on
		user_profile.id = master.user_profile_id
	left join
		agg_master_approvals
	on
		agg_master_approvals.master_id = master.id
	left join
		avg_master_rating
	on
		avg_master_rating.master_id = master.id
;


create table master_rating (
	-- user who rates
	user_profile_id int references user_profile(id) on delete cascade not null,
	-- rated master
	master_id int references master(id) on delete cascade not null,
	rating smallint not null,
	unique(user_profile_id, master_id)
);


-- create table master_comment (
-- 	user_profile_id int references user_profile(id) on delete cascade not null,
-- 	master_id int references master(id) on delete cascade not null,
-- 	created_at timestamptz not null default now(),
-- 	body text
-- );


create table master_approve_request (
	master_id int references master(id) on delete cascade unique not null,
	state text,
	reason text,
	created_at timestamptz not null default now(),
	unique(master_id)
);

create table master_approvals (
	user_profile_id int references user_profile(id) on delete cascade not null,
	master_id int references master(id) on delete cascade not null,
	created_at timestamptz not null default now(),
	unique (user_profile_id, master_id)
);


	







create table playing_group (
	id serial primary key,
	master_id int references master(id) on delete set null,

	-- users_id int[],
	-- messages_id int[],

	title text,
	description text,
	created_at timestamptz not null default now(),
	unique(title)
);

select
	array_agg(user_profile_id order by created_at) as user_profiles_id, 
	group_id
from
	lnk_group_user
group by
	group_id
;


select
	json_agg(
		group_message.*
		order by created_at
	) as messages,
	group_id
from
	group_message
group by
	group_id
-- order by created_at
;

create view view_group as
	with users as (
		select
			array_agg(user_profile_id order by created_at) as user_profiles_id,
			group_id
		from
			lnk_group_user
		group by
			group_id
			
	), messages as (
		select
			json_agg(
				group_message.*
				order by created_at
			) as messages,
			group_id
		from
			group_message
		group by
			group_id
	)
	select
		playing_group.*,
		messages.messages,
		users.user_profiles_id
	from
		playing_group
	left join
		users
	on
		users.group_id = playing_group.id
	left join
		messages
	on
		messages.group_id = playing_group.id
;


with profile as (
	select
		user_profile.id user_profile_id,
		master.id master_id
	from
		user_profile
	left join
		master
	on master.user_profile_id = user_profile.id
	where
		real_id = 64
)
insert into
	playing_group
		(master_id, title, description)
-- values
	(select profile.master_id, 'wrwer', 'desc' from profile)
returning *
;


with profile as (
	select
		user_profile.id user_profile_id,
		master.id master_id
	from
		user_profile
	left join
		master
	on master.user_profile_id = user_profile.id
	where
		real_id = 1
), related_users as (
	select
		lnk_group_user.group_id 
		-- user_profile.id as user_profile_id
	from
		lnk_group_user
	left join
		profile
	on
		lnk_group_user.user_profile_id = profile.user_profile_id
)
select 
	playing_group.*
from
	playing_group
where
	playing_group.master_id = (select master_id from profile)
		or
	id = (select group_id from related_users)
;

create table lnk_group_user (
	user_profile_id int references user_profile(id) on delete cascade,
	group_id int references playing_group(id) on delete cascade,
	created_at timestamptz not null default now(),
	unique(user_profile_id, group_id)
);


create table group_membership_request (
	id serial primary key,
	user_profile_id int references user_profile(id) on delete cascade,
	group_id int references playing_group(id) on delete cascade,
	created_at timestamptz not null default now(),
	state text,
	is_accepted bool not null default false,
	unique(user_profile_id, group_id)
);


create table group_message (
	id serial primary key,
	group_id int references playing_group(id) on delete cascade,
	owner_profile_id int references user_profile(id) on delete set null,
	created_at timestamptz not null default now(),

	body text
);






-- create table fraction (
-- 	id serial primary key,
-- 	created_at timestamptz not null default now(),
-- 	title text,

-- 	goals text,
-- 	description text

-- );


-- create table fraction_message (
-- 	fraction_id int references fraction(id) not null on delete cascade,
-- 	created_at timestamptz not null default now(),
-- 	body text not null,
-- 	signature text not null
-- );


-- create table fraction_desired_location (
-- 	fraction_id int references fraction(id) not null on delete cascade,
-- 	location_id int not null,
-- 	desired_thread_id int,
-- 	desired_perk_id int,
-- 	description text,
-- 	unique (fraction_id, location_id)
-- );


-- create table fraction_highlited_quest (
-- 	fraction_id int references fraction(id) not null on delete cascade,
-- 	quest_id int not null,
-- 	unique (fraction_id, quest_id)
-- );


-- create table lnk_fraction_user (
-- 	fraction_id int references fraction(id) not null on delete cascade,
--  	user_profile_id int references user_profile(id) not null on delete cascade,
-- 	role text,
-- 	unique (fraction_id, user_profile_id)
-- );


-- create table master_fraction_request (
-- 	master_id int references master(id) not null on delete cascade,
-- 	fraction_id int references fraction(id) not null on delete cascade,
-- 	is_closed boolean not null default false,
-- 	unique (master_id, fraction_id)
-- );


-- create lnk_fraction_master (
-- 	master_id int references master(id) not null on delete cascade unique,
-- 	fraction_id int references fraction(id) not null on delete cascade,
-- 	is_pinned boolean not null default false,

-- );
