CREATE TABLE public.vehicle (
    id integer NOT NULL,
    "created" timestamp without time zone NOT NULL,
    "modified" timestamp without time zone,
    name character varying(100) NOT NULL,
    category character varying(100) NOT NULL,
    registration_number character varying(100) NOT NULL,
    identification_number character varying(100) NOT NULL
);


CREATE SEQUENCE public.vehicle_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ONLY public.vehicle ALTER COLUMN id SET DEFAULT nextval('public.vehicle_id_seq'::regclass);
