<request>
	<target>Make PowerBI dashboard in pbip format, using input data file</target>
	<description>It is needed to make PowerBI dashboars, uses input md file like design concept, csv file as source data and produce output</description>
	<inputs>
		<input>
			<file_path>datasets/fin_sample_analysis_result.md</file_path>
			<description>File contains the dashboard design concept</description>
		</input>
		<input>
			<file_path>datasets/Financial Sample.csv</file_path>
			<description>File contains source data</description>
		</input>
	</inputs>
	<output>
		<folder_path>datasets/dashboard</folder_path>
		<description>PowerBI dashboard in PBIP format</description>
	</output>
	<action>Reach the target</action>
</request>