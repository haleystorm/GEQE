import syssys.path.append(".")import confimport jsonimport tangeloimport osimport timeimport datetimeimport commandlineLauncherdef generate_job_name():    """ generate a job id based on the current time """    return 'job_'+str(datetime.datetime.now()).replace(' ','_')@tangelo.restfuldef get(filePath='./',filePolygon='polyFile.txt',fileAppOut='appliedScores.csv',        fScoreThresh='0.005',        dataSet='',        useML="true", useBayes="false", nFeatures="300", custStopWord=""):    if filePath[-1] != '/': filePath = filePath+"/"    timeStamp = str(time.time())    ssName = filePath + "applyScores_" + timeStamp + ".sh"    useML = "true" == useML    # load the correct dataset by name from the data set config file    confObj = conf.get()    dataSetDict = confObj['datasets']    sparkSettings = confObj['spark']    if dataSet not in dataSetDict:        raise ValueError("Data set not found in conf. "+dataSet)    dataSetObj = dataSetDict[dataSet]    dataSetName = dataSet    dataSetPath = dataSetObj['path']    dataSetType = dataSetObj['type']    cleanCustStop = custStopWord.replace(" ","").replace("\"","\\\"")    algorithm = "aynWald_fsp.py" if useML else "findSimilarPlaces.py"    # deploy using spark submit    launchCommand = [ sparkSettings['SPARK_SUBMIT_PATH']+"spark-submit",                         "--py-files",                         "lib/shapeReader.py,lib/pointClass.py,lib/fspLib.py",                         "--executor-memory", sparkSettings['EXECUTOR_MEMORY'],                         "--driver-memory", sparkSettings['DRIVER_MEMORY'],                         "--total-executor-cores",sparkSettings['TOTAL_EXECUTOR_CORES'],                         algorithm,                         sparkSettings['SPARK_MASTER'],                         dataSetPath    ]    if  'aws-emr' == confObj['deploy-mode'] :        launchCommand.append('poly')        launchCommand.append('dict')        launchCommand.append('score')    else:        launchCommand.append("inputFiles/"+filePolygon)        launchCommand.append("dict_"+fileAppOut)        launchCommand.append(filePath+"/scoreFiles/"+fileAppOut)    launchCommand.extend(["-jobNm","geqe-run",                         "-datTyp",str(dataSetType),                         "-sThresh",fScoreThresh,                         "-sCustStop", "\"" + cleanCustStop + '\"',                         "--sit"    ])    if useML: launchCommand.extend(["-nFeatures", nFeatures])    if useML and useBayes != "false": launchCommand.append("--useBayes")    if 'local' == confObj['deploy-mode'] or 'cluster' == confObj['deploy-mode']:        jobname = generate_job_name()        commandlineLauncher.runCommand(jobname,launchCommand,filePath)        return jobname    elif 'aws-emr' == confObj['deploy-mode']:        import awsutil        jobname = generate_job_name()        jobconf = {}        jobconf['run_command'] = launchCommand        jobconf['dict_save_path'] =  filePath+'dictFiles/dict_'+fileAppOut        jobconf['score_save_path'] = filePath+'scoreFiles/'+fileAppOut        awsutil.submitJob(jobname,jobconf,filePath+'inputFiles/'+filePolygon)        tangelo.log("Submited job to aws. "+jobname)        return jobname    else:        raise Exception("Invalid deploy mode in conf.json.  should be local cluster or aws-emr")