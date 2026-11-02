// Trainer AI category test. run_ai_test.sh includes this file at the end of
// src/main.c's includes and calls TestAi() once at boot, before the main loop.
//
// Each scenario puts the AI's Pokemon (battler 1) against a target (battler 0)
// with the given types, Attack / Sp. Atk and last used move, then runs the AI's
// "check viability" script AI_TEST_TRIALS times. gTestAiScore holds the summed
// score of each of the AI's four moves (each trial starts every move at 100).
#include "battle.h"
#include "battle_ai_script_commands.h"
#include "random.h"
#include "constants/battle.h"
#include "constants/moves.h"
#include "constants/pokemon.h"
#include "ewram.h"
extern u16 gBattleTypeFlags;
extern u8 gActiveBattler;
extern u8 gBattlersCount;
extern u8 gBattlerPositions[MAX_BATTLERS_COUNT];
extern u8 gAbsentBattlerFlags;
extern u16 gLastMoves[MAX_BATTLERS_COUNT];
extern struct BattlePokemon gBattleMons[MAX_BATTLERS_COUNT];

#define AI_TEST_TRIALS 256

struct AiTestScenario
{
    u8 type1, type2;
    u16 attack, spAttack;
    u16 lastMove;
    u16 moves[MAX_MON_MOVES];
};

// Keep in sync with SCENARIOS in ai_report.py
static const struct AiTestScenario sAiTestScenarios[] =
{
    // Gengar-like: Ghost/Poison types (old "physical" types), but a special attacker
    {TYPE_GHOST, TYPE_POISON,  85, 150, MOVE_NONE,        {MOVE_REFLECT, MOVE_LIGHT_SCREEN, MOVE_GROWL, MOVE_TACKLE}},
    // Gyarados-like: Water/Flying (one old "special" and one old "physical" type), a physical attacker
    {TYPE_WATER, TYPE_FLYING, 145,  80, MOVE_NONE,        {MOVE_REFLECT, MOVE_LIGHT_SCREEN, MOVE_GROWL, MOVE_TACKLE}},
    // The target just used Shadow Ball (Ghost: old physical, now special)
    {TYPE_GHOST, TYPE_POISON,  85, 150, MOVE_SHADOW_BALL, {MOVE_COUNTER, MOVE_TACKLE, MOVE_GROWL, MOVE_TAIL_WHIP}},
    // The target just used Crunch (Dark: old special, now physical)
    {TYPE_ROCK,  TYPE_DARK,   154, 115, MOVE_CRUNCH,      {MOVE_MIRROR_COAT, MOVE_TACKLE, MOVE_GROWL, MOVE_TAIL_WHIP}},
    // The reverse pairs: moves the counter-move does work against now
    {TYPE_ROCK,  TYPE_DARK,   154, 115, MOVE_CRUNCH,      {MOVE_COUNTER, MOVE_TACKLE, MOVE_GROWL, MOVE_TAIL_WHIP}},
    {TYPE_GHOST, TYPE_POISON,  85, 150, MOVE_SHADOW_BALL, {MOVE_MIRROR_COAT, MOVE_TACKLE, MOVE_GROWL, MOVE_TAIL_WHIP}},
};

s32 gTestAiScore[ARRAY_COUNT(sAiTestScenarios)][MAX_MON_MOVES];

// run_ai_test.sh stops here to read gTestAiScore
void TestAiDone(void)
{
}

static void TestAiSetupMon(struct BattlePokemon *mon)
{
    u32 i;

    memset(mon, 0, sizeof(*mon));
    mon->species = 1;
    mon->level = 50;
    mon->hp = mon->maxHP = 150;
    mon->attack = mon->defense = mon->speed = mon->spAttack = mon->spDefense = 100;
    for (i = 0; i < 8; i++)
        mon->statStages[i] = 6;
}

void TestAi(void)
{
    u32 s, t, i;

    gRngValue = 0x12345678; // same random numbers for every build
    for (s = 0; s < ARRAY_COUNT(sAiTestScenarios); s++)
    {
        const struct AiTestScenario *sc = &sAiTestScenarios[s];

        for (i = 0; i < MAX_MON_MOVES; i++)
            gTestAiScore[s][i] = 0;
        for (t = 0; t < AI_TEST_TRIALS; t++)
        {
            memset(gDisableStructs, 0, sizeof(gDisableStructs));
            gBattleTypeFlags = BATTLE_TYPE_TRAINER;
            gBattlersCount = 2;
            gBattlerPositions[0] = B_POSITION_PLAYER_LEFT;
            gBattlerPositions[1] = B_POSITION_OPPONENT_LEFT;
            gAbsentBattlerFlags = 0;

            TestAiSetupMon(&gBattleMons[0]); // the target
            gBattleMons[0].type1 = sc->type1;
            gBattleMons[0].type2 = sc->type2;
            gBattleMons[0].attack = sc->attack;
            gBattleMons[0].spAttack = sc->spAttack;
            gLastMoves[0] = sc->lastMove;

            TestAiSetupMon(&gBattleMons[1]); // the AI's Pokemon
            for (i = 0; i < MAX_MON_MOVES; i++)
            {
                gBattleMons[1].moves[i] = sc->moves[i];
                gBattleMons[1].pp[i] = 20;
            }
            gLastMoves[1] = MOVE_NONE;

            gActiveBattler = 1;
            BattleAI_SetupAIData();
            AI_THINKING_STRUCT->aiFlags = 1 << 1; // only the "check viability" script
            BattleAI_GetAIActionToUse();
            for (i = 0; i < MAX_MON_MOVES; i++)
                gTestAiScore[s][i] += AI_THINKING_STRUCT->score[i];
        }
    }
    TestAiDone();
}
