table_ = '''CREATE TABLE public.user_login (
	user_id varchar NOT NULL,
	CONSTRAINT user_login_unique UNIQUE (user_id)
);'''


ins_cred = '''INSERT INTO public.login_credetials
(client_id, s_password)
VALUES(%s, %s) on conflict Do nothing;'''


saved_data_fetch = '''
select
	distinct j_extracted_data::jsonb
from
	tbl_registered_user tru
where
	client_id = '%s';
'''