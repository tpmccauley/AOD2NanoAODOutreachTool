import FWCore.ParameterSet.Config as cms
import FWCore.Utilities.FileUtils as FileUtils
import FWCore.PythonUtilities.LumiList as LumiList
import FWCore.ParameterSet.Types as CfgTypes

process = cms.Process("AOD2NanoAOD")
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = "WARNING"
process.MessageLogger.categories.append("AOD2NanoAOD")

process.MessageLogger.cerr.INFO = cms.untracked.PSet(
    limit=cms.untracked.int32(-1)
)

process.options = cms.untracked.PSet(
    wantSummary=cms.untracked.bool(True)
)

# Set the maximum number of events to be processed (-1 processes all events)
process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32(1000))

goodJSON = 'data/Cert_13TeV_16Dec2015ReReco_Collisions15_25ns_JSON_v2.txt'
myLumis = LumiList.LumiList(filename = goodJSON).getCMSSWString().split(',') 

process.GlobalTag.globaltag = '76X_dataRun2_16Dec2015_v0'

data_files = FileUtils.loadListFromFile('data/CMS_Run2015D_MuonEG_AOD_16Dec2015-v1_00000_file_index.txt') 

process.source = cms.Source(
    "PoolSource", fileNames=cms.untracked.vstring(*data_files)
)

# Number of events to be skipped (0 by default)
process.source.skipEvents = cms.untracked.uint32(0)

# Register fileservice for output file
process.aod2nanoaod = cms.EDAnalyzer(
    "AOD2NanoAOD"
)

process.TFileService = cms.Service(
    "TFileService", fileName=cms.string("MuonEG_Run2015D_nanoAOD.root")
)

process.p = cms.Path(process.aod2nanoaod)
