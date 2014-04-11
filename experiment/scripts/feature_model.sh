LearnerZ3  \
    --numinstances=-1 \
    --testset=2 \
    --learningiterations=3 \
    --cores=4  \
    --experimentnumsplits  8 \
    --parametersfile parameters/feature_model.parameters \
    --generatorfile generators/feature_model.cfr \
    --formatter formatters/feature_model_formatter.py \
    --heuristics heuristics/feature_model.heuristics \
    --outputdirectory runs/test/  
