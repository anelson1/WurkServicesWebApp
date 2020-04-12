--
-- PostgreSQL database dump
--

-- Dumped from database version 12.2
-- Dumped by pg_dump version 12.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: bookings; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bookings (
    bid character varying(20),
    stuname character varying(20),
    teachername character varying(20),
    tob character varying(20)
);


ALTER TABLE public.bookings OWNER TO postgres;

--
-- Name: bookingtimes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.bookingtimes (
    bid character varying(20),
    month character varying(20),
    day character varying(20),
    starttime character varying(20),
    endtime character varying(20)
);


ALTER TABLE public.bookingtimes OWNER TO postgres;

--
-- Name: code; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.code (
    name character varying(20),
    password character varying(20)
);


ALTER TABLE public.code OWNER TO postgres;

--
-- Name: teacher; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.teacher (
    tid character varying(255) NOT NULL,
    firstname character varying(255),
    lastname character varying(255),
    typeofteacher character varying(20)
);


ALTER TABLE public.teacher OWNER TO postgres;

--
-- Name: teacherbook; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.teacherbook (
    tid character varying(255),
    month character varying(20),
    day character varying(20),
    starttime character varying(20),
    endtime character varying(20)
);


ALTER TABLE public.teacherbook OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    username character varying(20) NOT NULL,
    password character varying(20),
    email character varying(40),
    phonenumber character varying(40),
    address character varying(40),
    city character varying(30),
    state character varying(30),
    firstname character varying(30),
    lastname character varying(30),
    istutor boolean
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Data for Name: bookings; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.bookings (bid, stuname, teachername, tob) FROM stdin;
V4lFhc	Piss Mgee	CocknBall	\N
aoMDNA	Piss Mgee	CocknBall	\N
C4brIg	Piss Mgee	CocknBall	\N
vCRrqp	Piss Mgee	CocknBall	\N
tl5Wtw	Piss Mgee	CocknBall	\N
trxZwx	Piss Mgee	CocknBall	\N
1fff3Y	Deanna Nelson	CocknBall	\N
z7k9wh	Todd Dickson	CocknBall	\N
6t4oCj	sdfsd		landscaping
yaMp84	sdfsd		landscaping
X5d96L	2		pet
Y8f9L0	2		pet
E7oe4z	Tito Tester		house
7oIVyT	453		Sports Coaching
ziJ0Pz	jkjk	Angelo	ACT and SAT Prep
ar7Uhg	Sauce Boss		Landscaping
\.


--
-- Data for Name: bookingtimes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.bookingtimes (bid, month, day, starttime, endtime) FROM stdin;
V4lFhc	jan	1	7am	8am
aoMDNA	jan	1	7am	8am
C4brIg	jan	1	7am	8am
vCRrqp	jan	1	7am	8am
tl5Wtw	jan	1	7am	8am
trxZwx	jan	1	7am	8am
1fff3Y	jan	1	1am	2am
z7k9wh	jan	1	7am	8am
6t4oCj	January	1	9am	\N
yaMp84	January	1	9am	\N
X5d96L	January	1	12pm	\N
Y8f9L0	January	1	12pm	\N
E7oe4z	July	4	2pm	\N
7oIVyT	Febuary	3	1pm	\N
ziJ0Pz	April	1	1am	2am
ar7Uhg	January	1	12pm	\N
\.


--
-- Data for Name: code; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.code (name, password) FROM stdin;
jim	123
\.


--
-- Data for Name: teacher; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.teacher (tid, firstname, lastname, typeofteacher) FROM stdin;
1	CocknBall	Torture	\N
2	Tito	Teacher	\N
9pQ1x7	Angelo	Nelson	ACT and SAT Prep
\.


--
-- Data for Name: teacherbook; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.teacherbook (tid, month, day, starttime, endtime) FROM stdin;
9pQ1x7	April	1	1	2
9pQ1x7	April	1	2	3
9pQ1x7	April	1	3	4
9pQ1x7	April	1	4	5
9pQ1x7	April	1	5	6
9pQ1x7	April	1	6	7
9pQ1x7	April	1	7	8
9pQ1x7	April	1	8	9
9pQ1x7	April	1	9	10
9pQ1x7	April	1	10	11
9pQ1x7	April	1	11	12
1	January	1	1	2
1	January	1	2	3
1	January	1	3	4
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (username, password, email, phonenumber, address, city, state, firstname, lastname, istutor) FROM stdin;
ajx1999	Aj1357911	angelonelson@outlook.com	8474187120	4 three lakes rd	Barrington	Illinois	Angelo	Nelson	\N
									\N
games	123	piss	piss	piss	piss	piss	Tito	Dick	\N
123	123	Piss	847-418-7120	4 three lakes rd	Barrington	Illinois	Piss	Mckenzie	\N
thoward	123	angelo@nelson.com	847-444-4444	32 Piss lane	Pissville	AL	Todd	Howard	\N
admin	nibbabehiminey	\N	\N	\N	\N	\N	\N	\N	\N
\.


--
-- Name: teacher teacher_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.teacher
    ADD CONSTRAINT teacher_pkey PRIMARY KEY (tid);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (username);


--
-- PostgreSQL database dump complete
--

