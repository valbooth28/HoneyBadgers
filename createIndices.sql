--Schools indices
--We filter by both State and type.
CREATE INDEX school1 ON School (State, Type);
--OPE_ID shhould be unique for School, as this is just info about the school
-- OPE_ID is used in the join to FAFSA_Data
CREATE UNIQUE INDEX school2 ON School(OPE_ID);


--FAFSA_Data indices
--OPE_ID is used to join on the school table, Y_(In)Dependent is summed, we 
--filter by Qtr or search for Q6, and filter by year.
CREATE INDEX faf1 ON FAFSA_Data (OPE_ID,Y_Dependent,Y_Independent,Qtr, Year);