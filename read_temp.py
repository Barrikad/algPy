from machine import Pin
from machine import ADC
from machine import DAC
from math import log

import machine
import utime

adc_V_lookup = [0.02470588, 0.02058824, 0.04117647, 0.06176471, 0.06588235, 0.07, 0.07411765, 0.07720589, 0.08029412, 0.08338236, 0.08647059, 0.09058825, 0.09470588, 0.09882354, 0.1019118, 0.105, 0.1080882, 0.1111765, 0.1152941, 0.1194118, 0.1235294, 0.1266177, 0.1297059, 0.1327941, 0.1358824, 0.1389706, 0.1420588, 0.1451471, 0.1482353, 0.1513235, 0.1544118, 0.1575, 0.1605882, 0.1647059, 0.1688235, 0.1729412, 0.1760294, 0.1791177, 0.1822059, 0.1852941, 0.1883824, 0.1914706, 0.1945588, 0.1976471, 0.2017647, 0.2058824, 0.21, 0.2130883, 0.2161765, 0.2192647, 0.222353, 0.2264706, 0.2305882, 0.2347059, 0.2377941, 0.2408824, 0.2439706, 0.2470588, 0.2511765, 0.2552941, 0.2594118, 0.2625, 0.2655883, 0.2686765, 0.2717647, 0.274853, 0.2779412, 0.2810294, 0.2841177, 0.2872059, 0.2902942, 0.2933824, 0.2964706, 0.2995588, 0.3026471, 0.3057353, 0.3088235, 0.3129412, 0.3170588, 0.3211765, 0.3242647, 0.327353, 0.3304412, 0.3335294, 0.3376471, 0.3417647, 0.3458824, 0.3489706, 0.3520588, 0.3551471, 0.3582353, 0.3613235, 0.3644118, 0.3675, 0.3705883, 0.3747059, 0.3788235, 0.3829412, 0.3870588, 0.3911765, 0.3952941, 0.3977647, 0.4002353, 0.4027059, 0.4051764, 0.4076471, 0.4117647, 0.4158824, 0.42, 0.4230883, 0.4261765, 0.4292647, 0.432353, 0.4364706, 0.4405883, 0.4447059, 0.4477942, 0.4508824, 0.4539706, 0.4570589, 0.4601471, 0.4632353, 0.4663236, 0.4694118, 0.4735294, 0.4776471, 0.4817647, 0.4842353, 0.4867059, 0.4891765, 0.4916471, 0.4941177, 0.4972059, 0.5002942, 0.5033824, 0.5064706, 0.5105882, 0.5147059, 0.5188236, 0.5219118, 0.525, 0.5280883, 0.5311765, 0.5352941, 0.5394118, 0.5435295, 0.5466177, 0.5497059, 0.5527942, 0.5558824, 0.56, 0.5641177, 0.5682353, 0.5713236, 0.5744118, 0.5775001, 0.5805883, 0.5836765, 0.5867648, 0.589853, 0.5929412, 0.5960294, 0.5991177, 0.6022058, 0.6052941, 0.6094118, 0.6135294, 0.6176471, 0.6207353, 0.6238235, 0.6269117, 0.63, 0.6341177, 0.6382353, 0.642353, 0.6454412, 0.6485294, 0.6516176, 0.6547059, 0.6588235, 0.6629412, 0.6670588, 0.670147, 0.6732353, 0.6763235, 0.6794118, 0.6825, 0.6855883, 0.6886765, 0.6917647, 0.6948529, 0.6979412, 0.7010294, 0.7041177, 0.7072059, 0.7102942, 0.7133823, 0.7164706, 0.7195588, 0.7226471, 0.7257353, 0.7288236, 0.7329412, 0.7370589, 0.7411765, 0.7442647, 0.747353, 0.7504412, 0.7535295, 0.757647, 0.7617648, 0.7658824, 0.7689706, 0.7720589, 0.7751471, 0.7782353, 0.7813235, 0.7844118, 0.7875, 0.7905883, 0.7947059, 0.7988235, 0.8029412, 0.8060294, 0.8091177, 0.8122059, 0.8152942, 0.8194118, 0.8235294, 0.8276471, 0.8307353, 0.8338236, 0.8369118, 0.8400001, 0.8441177, 0.8482353, 0.852353, 0.8548235, 0.8572942, 0.8597647, 0.8622354, 0.8647059, 0.8688236, 0.8729412, 0.8770589, 0.8801471, 0.8832354, 0.8863235, 0.8894118, 0.8925, 0.8955883, 0.8986765, 0.9017648, 0.9042353, 0.906706, 0.9091764, 0.9116471, 0.9141177, 0.9182354, 0.9223529, 0.9264707, 0.9295588, 0.9326471, 0.9357353, 0.9388236, 0.9419118, 0.9450001, 0.9480883, 0.9511765, 0.9542647, 0.957353, 0.9604412, 0.9635295, 0.9676472, 0.9717647, 0.9758824, 0.9789706, 0.9820589, 0.9851471, 0.9882354, 0.9913236, 0.9944118, 0.9975, 1.000588, 1.003677, 1.006765, 1.009853, 1.012941, 1.017059, 1.021176, 1.025294, 1.028382, 1.031471, 1.034559, 1.037647, 1.040735, 1.043824, 1.046912, 1.05, 1.054118, 1.058235, 1.062353, 1.065441, 1.068529, 1.071618, 1.074706, 1.077794, 1.080882, 1.083971, 1.087059, 1.090147, 1.093235, 1.096324, 1.099412, 1.103529, 1.107647, 1.111765, 1.114853, 1.117941, 1.121029, 1.124118, 1.127206, 1.130294, 1.133382, 1.136471, 1.140588, 1.144706, 1.148824, 1.151912, 1.155, 1.158088, 1.161177, 1.164265, 1.167353, 1.170441, 1.17353, 1.176618, 1.179706, 1.182794, 1.185882, 1.19, 1.194118, 1.198235, 1.201324, 1.204412, 1.2075, 1.210588, 1.214706, 1.218824, 1.222941, 1.225412, 1.227882, 1.230353, 1.232824, 1.235294, 1.239412, 1.243529, 1.247647, 1.250735, 1.253824, 1.256912, 1.26, 1.263088, 1.266176, 1.269265, 1.272353, 1.276471, 1.280588, 1.284706, 1.287794, 1.290882, 1.293971, 1.297059, 1.300147, 1.303235, 1.306324, 1.309412, 1.3125, 1.315588, 1.318676, 1.321765, 1.325882, 1.33, 1.334118, 1.336588, 1.339059, 1.341529, 1.344, 1.346471, 1.349559, 1.352647, 1.355735, 1.358824, 1.361912, 1.365, 1.368088, 1.371176, 1.375294, 1.379412, 1.383529, 1.386618, 1.389706, 1.392794, 1.395882, 1.4, 1.404118, 1.408235, 1.411324, 1.414412, 1.4175, 1.420588, 1.424706, 1.428824, 1.432941, 1.436029, 1.439118, 1.442206, 1.445294, 1.448382, 1.451471, 1.454559, 1.457647, 1.460735, 1.463824, 1.466912, 1.47, 1.474118, 1.478235, 1.482353, 1.485441, 1.488529, 1.491618, 1.494706, 1.497794, 1.500882, 1.503971, 1.507059, 1.510147, 1.513235, 1.516324, 1.519412, 1.5225, 1.525588, 1.528677, 1.531765, 1.535882, 1.54, 1.544118, 1.547206, 1.550294, 1.553382, 1.556471, 1.560588, 1.564706, 1.568824, 1.571912, 1.575, 1.578088, 1.581177, 1.585294, 1.589412, 1.593529, 1.596618, 1.599706, 1.602794, 1.605882, 1.608971, 1.612059, 1.615147, 1.618235, 1.622353, 1.626471, 1.630588, 1.633677, 1.636765, 1.639853, 1.642941, 1.647059, 1.651177, 1.655294, 1.658382, 1.661471, 1.664559, 1.667647, 1.670735, 1.673824, 1.676912, 1.68, 1.683088, 1.686177, 1.689265, 1.692353, 1.696471, 1.700588, 1.704706, 1.707794, 1.710882, 1.713971, 1.717059, 1.721177, 1.725294, 1.729412, 1.7325, 1.735588, 1.738677, 1.741765, 1.744853, 1.747941, 1.751029, 1.754118, 1.756588, 1.759059, 1.76153, 1.764, 1.766471, 1.770588, 1.774706, 1.778824, 1.781912, 1.785, 1.788088, 1.791177, 1.795294, 1.799412, 1.80353, 1.806618, 1.809706, 1.812794, 1.815882, 1.818971, 1.822059, 1.825147, 1.828235, 1.831324, 1.834412, 1.8375, 1.840588, 1.844706, 1.848824, 1.852941, 1.85603, 1.859118, 1.862206, 1.865294, 1.868382, 1.871471, 1.874559, 1.877647, 1.881765, 1.885882, 1.89, 1.893088, 1.896177, 1.899265, 1.902353, 1.90647, 1.910588, 1.914706, 1.917794, 1.920882, 1.923971, 1.927059, 1.931176, 1.935294, 1.939412, 1.941882, 1.944353, 1.946824, 1.949294, 1.951765, 1.955882, 1.96, 1.964118, 1.967206, 1.970294, 1.973382, 1.976471, 1.979559, 1.982647, 1.985735, 1.988824, 1.992941, 1.997059, 2.001177, 2.004265, 2.007353, 2.010441, 2.01353, 2.017647, 2.021765, 2.025882, 2.028971, 2.032059, 2.035147, 2.038235, 2.042353, 2.046471, 2.050588, 2.053677, 2.056765, 2.059853, 2.062941, 2.06603, 2.069118, 2.072206, 2.075294, 2.078382, 2.081471, 2.084559, 2.087647, 2.090735, 2.093824, 2.096912, 2.1, 2.104118, 2.108235, 2.112353, 2.115441, 2.11853, 2.121618, 2.124706, 2.127794, 2.130883, 2.133971, 2.137059, 2.140147, 2.143235, 2.146324, 2.149412, 2.153529, 2.157647, 2.161765, 2.164853, 2.167941, 2.17103, 2.174118, 2.177206, 2.180294, 2.183383, 2.186471, 2.188941, 2.191412, 2.193882, 2.196353, 2.198824, 2.202941, 2.207059, 2.211177, 2.214265, 2.217353, 2.220441, 2.22353, 2.226618, 2.229706, 2.232794, 2.235883, 2.238971, 2.242059, 2.245147, 2.248235, 2.252353, 2.256471, 2.260588, 2.263677, 2.266765, 2.269853, 2.272941, 2.27603, 2.279118, 2.282206, 2.285294, 2.288383, 2.291471, 2.294559, 2.297647, 2.301765, 2.305882, 2.31, 2.312471, 2.314941, 2.317412, 2.319882, 2.322353, 2.326471, 2.330588, 2.334706, 2.337794, 2.340883, 2.343971, 2.347059, 2.351177, 2.355294, 2.359412, 2.3625, 2.365588, 2.368677, 2.371765, 2.374853, 2.377941, 2.381029, 2.384118, 2.387206, 2.390294, 2.393382, 2.396471, 2.399559, 2.402647, 2.405735, 2.408823, 2.411912, 2.415, 2.418088, 2.421176, 2.424265, 2.427353, 2.430441, 2.433529, 2.436618, 2.439706, 2.442794, 2.445882, 2.448971, 2.452059, 2.455147, 2.458235, 2.461323, 2.464412, 2.4675, 2.470588, 2.473676, 2.476765, 2.479853, 2.482941, 2.486029, 2.489118, 2.492206, 2.495294, 2.498382, 2.501471, 2.504559, 2.507647, 2.510735, 2.513824, 2.516912, 2.52, 2.523088, 2.526176, 2.529265, 2.532353, 2.534824, 2.537294, 2.539765, 2.542235, 2.544706, 2.547794, 2.550882, 2.553971, 2.557059, 2.560147, 2.563235, 2.566324, 2.569412, 2.5725, 2.575588, 2.578676, 2.581765, 2.583824, 2.585882, 2.587941, 2.59, 2.592059, 2.594118, 2.596588, 2.599059, 2.60153, 2.604, 2.606471, 2.609559, 2.612647, 2.615735, 2.618824, 2.621912, 2.625, 2.628088, 2.631176, 2.634265, 2.637353, 2.640441, 2.643529, 2.645588, 2.647647, 2.649706, 2.651765, 2.653824, 2.655882, 2.658971, 2.662059, 2.665147, 2.668235, 2.670706, 2.673177, 2.675647, 2.678118, 2.680588, 2.683059, 2.685529, 2.688, 2.690471, 2.692941, 2.695412, 2.697882, 2.700353, 2.702824, 2.705294, 2.707765, 2.710235, 2.712706, 2.715177, 2.717647, 2.720118, 2.722588, 2.725059, 2.72753, 2.73, 2.732471, 2.734941, 2.737412, 2.739882, 2.742353, 2.744824, 2.747294, 2.749765, 2.752235, 2.754706, 2.756765, 2.758824, 2.760882, 2.762941, 2.765, 2.767059, 2.769529, 2.772, 2.774471, 2.776941, 2.779412, 2.781882, 2.784353, 2.786824, 2.789294, 2.791765, 2.793824, 2.795882, 2.797941, 2.8, 2.802059, 2.804118, 2.806588, 2.809059, 2.81153, 2.814, 2.816471, 2.81853, 2.820588, 2.822647, 2.824706, 2.826765, 2.828824, 2.830883, 2.832941, 2.835, 2.837059, 2.839118, 2.841177, 2.843647, 2.846118, 2.848588, 2.851059, 2.853529, 2.855588, 2.857647, 2.859706, 2.861765, 2.863824, 2.865882, 2.867941, 2.87, 2.872059, 2.874118, 2.876177, 2.878235, 2.88, 2.881765, 2.883529, 2.885294, 2.887059, 2.888824, 2.890588, 2.892353, 2.894118, 2.895882, 2.897647, 2.899412, 2.901177, 2.902941, 2.905, 2.907059, 2.909118, 2.911177, 2.913235, 2.915294, 2.917353, 2.919412, 2.921471, 2.92353, 2.925588, 2.927647, 2.929706, 2.931765, 2.933824, 2.935883, 2.937941, 2.94, 2.942059, 2.944118, 2.946177, 2.948236, 2.950294, 2.952353, 2.954118, 2.955883, 2.957647, 2.959412, 2.961176, 2.962941, 2.964706, 2.966765, 2.968824, 2.970882, 2.972941, 2.975, 2.977059, 2.978824, 2.980588, 2.982353, 2.984118, 2.985882, 2.987647, 2.989412, 2.991471, 2.99353, 2.995588, 2.997647, 2.999706, 3.001765, 3.00353, 3.005294, 3.007059, 3.008824, 3.010588, 3.012353, 3.014118, 3.015882, 3.017647, 3.019412, 3.021177, 3.022941, 3.024706, 3.026471, 3.02853, 3.030588, 3.032647, 3.034706, 3.036765, 3.038824, 3.040588, 3.042353, 3.044118, 3.045882, 3.047647, 3.049412, 3.051177, 3.052721, 3.054265, 3.055809, 3.057353, 3.058897, 3.060441, 3.061985, 3.063529, 3.065294, 3.067059, 3.068824, 3.070588, 3.072353, 3.074118, 3.075882, 3.077427, 3.078971, 3.080515, 3.082059, 3.083603, 3.085147, 3.086691, 3.088235, 3.090294, 3.092353, 3.094412, 3.096471, 3.098529, 3.100588, 3.102353, 3.104118, 3.105882, 3.107647, 3.109412, 3.111177, 3.112941, 3.114706, 3.116471, 3.118235, 3.12, 3.121765, 3.12353, 3.137647]

NOM_RES = 10000
SER_RES = 9820
TEMP_NOM = 25
NUM_SAMPLES = 25
THERM_B_COEFF = 3950
ADC_MAX = 1023
ADC_Vmax = 3.15

def init_temp_sensor(TENP_SENS_ADC_PIN_NO = 32):
    adc = ADC(Pin(TENP_SENS_ADC_PIN_NO))
    adc.atten(ADC.ATTN_11DB)
    adc.width(ADC.WIDTH_10BIT)
    return adc

def read_temp(temp_sens):
    raw_read = []
    # Collect NUM_SAMPLES
    for i in range(1, NUM_SAMPLES+1):
        raw_read.append(temp_sens.read())

    # Average of the NUM_SAMPLES and look it up in the table
    raw_average = sum(raw_read)/NUM_SAMPLES
    print('raw_avg = ' + str(raw_average))
    print('V_measured = ' + str(adc_V_lookup[round(raw_average)]))

    # Convert to resistance
    raw_average = ADC_MAX * adc_V_lookup[round(raw_average)]/ADC_Vmax
    resistance = (SER_RES * raw_average) / (ADC_MAX - raw_average)
    print('Thermistor resistance: {} ohms'.format(resistance))

    # Convert to temperature
    steinhart  = log(resistance / NOM_RES) / THERM_B_COEFF
    steinhart += 1.0 / (TEMP_NOM + 273.15)
    steinhart  = (1.0 / steinhart) - 273.15
    return steinhart

print("I'm alive!\n")
utime.sleep_ms(2000)

temp_sens = init_temp_sensor()

sample_last_ms = 0
SAMPLE_INTERVAL = 1000

while (True):
    if utime.ticks_diff(utime.ticks_ms(), sample_last_ms) >= SAMPLE_INTERVAL:
        temp = read_temp(temp_sens)
        print('Thermistor temperature: ' + str(temp))
        sample_last_ms = utime.ticks_ms()
