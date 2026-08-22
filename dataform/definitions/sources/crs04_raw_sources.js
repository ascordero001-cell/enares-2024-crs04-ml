const rawProject = dataform.projectConfig.vars.rawProject;
const rawDataset = dataform.projectConfig.vars.rawDataset;

[
  "raw_crs04_cap100",
  "raw_crs04_cap200",
  "raw_crs04_cap248",
  "raw_crs04_cap300",
].forEach((tableName) => {
  declare({
    database: rawProject,
    schema: rawDataset,
    name: tableName,
  });
});